# coding=utf-8
import sys
from datetime import datetime, timedelta

import string, os, re #urllib, zipfile, copy
from guessit import guessit
import dexml
from dexml import fields
OS_PLEX_USERAGENT = 'plexapp.com v9.0'

seriesList = {}

def Start():
    HTTP.CacheTime = 0
    HTTP.Headers['User-agent'] = OS_PLEX_USERAGENT
    Log("START CALLED")

def ValidatePrefs():
    return


# def logObject(obj):
#     Log("obj: %s" % str(obj))
#     for attr in dir(obj):
#         Log("obj.%s = %r" % (attr, getattr(obj, attr)))

class sr(dexml.Model):
    rlsid = fields.String()
    team = fields.String(tagname='team')
    fmt = fields.String(tagname='fmt')
    hits = fields.Integer(tagname='hits')
    duration_string = fields.String(tagname='duration')   
    dur=None
    
    def get_duration(self):
        if self.dur is None:
            try:
                timet1 = datetime.strptime(self.duration_string,"%H:%M:%S")
            except ValueError:
                timet1 = datetime.strptime(self.duration_string,"%M:%S")
            delta1 = timedelta(
                hours=timet1.time().hour,
                minutes=timet1.time().minute,
                seconds=timet1.time().second)
            self.dur = delta1.total_seconds()*1000
        return self.dur
    duration = property(get_duration)
        


def getSubUrl(data):
    show_title = findSeriesNameinXsubs(data.show_title)
    if show_title !='':
        srid = seriesList[show_title]
    else:
        Log("Couldn't find series in X-Subs. Plex Series Name: %s" % data.show_title)
        return

    seriesUrl = 'http://xsubs.tv/series/'+str(srid)+'/main.xml'
    Log(seriesUrl)

    elem = HTML.ElementFromURL(seriesUrl)    
    subpages = elem.xpath("//series_group[@ssnnum='"+data.season+"']/@ssnid")
    if len(subpages)==0:
        Log("Couldn't find season %s in X-Subs." % data.season)
        return

    Log("Retrieving Subtitles")
    ssnUrl = 'http://xsubs.tv/series/'+str(srid)+'/'+subpages[0]+'.xml'
    ssnElem = HTML.ElementFromURL(ssnUrl)
    subsElements = ssnElem.xpath("//subg[etitle[@number="+data.episode+"]]//sr[@published_on!='']")
    
    Log("Found %d subtitles" % len(subsElements))
    Log("Searching subtitles for source: %s | resolution: %s | release_group: %s | duration: %s" % (data.source, data.resolution, data.release_group, data.duration))
    srs = map(lambda x: sr.parse(HTML.StringFromElement(x)),subsElements)
    for srf in srs:
        Log("rlsid: %s | team: %s | fmt: %s  | hits: %s | duration: %s" % (srf.rlsid, srf.team, srf.fmt, srf.hits, srf.duration))
    
    Log("Searching explicit subtitle results")
    srs_filterd = filter(lambda x: (data.source in x.fmt.lower() and data.resolution in x.fmt.lower() and data.release_group in x.team.lower() and data.duration==x.duration)  ,srs)
    if len(srs_filterd) > 0:
        srs_filterd.sort(key=lambda x: x.hits, reverse=True)
        Log("Found %d explicit matching subtitles" % len(srs_filterd))
        for srf in srs_filterd:
            Log("rlsid: %s | team: %s | fmt: %s  | hits: %s | duration: %s" % (srf.rlsid, srf.team, srf.fmt, srf.hits, srf.duration))
    else:
        Log("Searching fuzzy subtitle results")
        srs_filterd = filter(lambda x: ((data.source in x.fmt.lower() or data.resolution in x.fmt.lower()) and data.release_group==x.team) or ((data.source in x.fmt.lower() or data.resolution in x.fmt.lower()) and data.duration==x.duration) ,srs)
        srs_filterd.sort(key=lambda x: x.hits, reverse=True)
        Log("Found %d fuzzy matching subtitles" % len(srs_filterd))
        for srf in srs_filterd:
            Log("rlsid: %s | team: %s | fmt: %s  | hits: %s | duration: %s" % (srf.rlsid, srf.team, srf.fmt, srf.hits, srf.duration))
    if len(srs_filterd) > 0:
        return 'http://xsubs.tv/xthru/getsub/'+ srs_filterd[0].rlsid
    Log("Searching only by source (Blu-ray, Web-dl, etc) subtitle results")
    srs_filterd = filter(lambda x: (data.source in x.fmt.lower()) ,srs)
    srs_filterd.sort(key=lambda x: x.hits, reverse=True)
    Log("Found %d only by source (Blu-ray, Web-dl, etc) matching subtitles" % len(srs_filterd))
    for srf in srs_filterd:
        Log("rlsid: %s | team: %s | fmt: %s  | hits: %s | duration: %s" % (srf.rlsid, srf.team, srf.fmt, srf.hits, srf.duration))
    if len(srs_filterd) > 0:
        return 'http://xsubs.tv/xthru/getsub/'+ srs_filterd[0].rlsid
    return ""
    

def RetrieveSeriesList():
    Log("Retrieving Series list from X-Subs")
    seriesUrl = 'http://xsubs.tv/series/all.xml'
    elem = HTML.ElementFromURL(seriesUrl)
    subpages = elem.xpath("//series")
    for l in subpages:
        seriesList[l.xpath('./text()')[0]] = int(l.xpath('./@srsid')[0])
    Log("Retrieved All Series successfully")


def findSeriesNameinXsubs(name):
    Log("Searching the Plex Series Name: %s in the X-Subs Series List" % name)
    # try removing parenthesees in given name
    tmpName = name
    tmpName = re.sub(r'\([^)]*\)', '', tmpName).strip()
    sName  = string.split(tmpName,' ')
    srchName = []
    fnlName = ''
    if sName[0].lower() == 'the':
        for i in range(1,len(sName)):
            srchName.append(sName[i])
        #Log(srchName)
        srchName.append('(The)')
        #Log(srchName)
        fnlName  = ' '.join(srchName)
        #Log(fnlName)
    else:
        fnlName = tmpName
    if fnlName in seriesList:
        Log("Found series in X-Subs with X-Subs Name: %s" % fnlName)
        return fnlName
    for key, value in seriesList.iteritems():
        if re.sub(r'\[[^)]*\]', '', key).lower().strip() == fnlName.lower():
            Log("Found series in X-Subs with X-Subs Name: %s" % key)
            return key


    tmpDict = {}
    splName  = string.split(name,' ')
    for key, value in seriesList.iteritems():
        for wrd in splName:
            if len(wrd)<3:
                continue
            if wrd=='' or wrd.lower()=='the'or wrd.lower()=='and':
                continue
            if wrd in key:
                if key in tmpDict:
                    tmpDict[key].append(wrd)
                else:
                    tmpDict[key] = [wrd]
    count = 0
    hgName = ''
    for key,value in tmpDict.iteritems():
        if len(value)> count:
            count = len(value)
            hgName = key
    if count > 1:
        Log("Found series in X-Subs with X-Subs Name: %s" % hgName)
        return hgName
    return ''



class EpisodeData(object):
  def __init__(self, show_title, season, episode, duration, resolution, source, release_group):
    self.show_title = show_title
    self.season = season
    self.episode = episode
    delta2 = timedelta(milliseconds=int(duration))
    delta3 = timedelta(
        seconds=delta2.seconds)
    self.duration = delta3.total_seconds()*1000
    self.resolution = resolution
    self.source = source.lower()
    self.release_group = release_group.lower()

def LoggedIn():
    forum = HTML.ElementFromURL("http://xsubs.tv/xforum/")
    a = forum.xpath("//a[@href='/xforum/account/signin/']")
    if len(a) > 0:
        return False
    return True

def LogIn():
    forum = HTML.ElementFromURL("http://xsubs.tv/xforum/account/signin/")
    csrfmiddlewaretoken = forum.xpath("//input[@name='csrfmiddlewaretoken']/@value")[0]
    values = {'csrfmiddlewaretoken' : csrfmiddlewaretoken,
          'username' : Prefs["xsubs.username"],
          'password' : Prefs["xsubs.password"] ,
          'next' : '' }
    forum = HTML.ElementFromURL("http://xsubs.tv/xforum/account/signin/", values, method="POST")

class XsubsSubtitlesAgentTvShows(Agent.TV_Shows):
    name = 'Xsubs TV Subtitles'
    languages = [Locale.Language.Greek]
    primary_provider = False
    contributes_to = ['com.plexapp.agents.thetvdb']

    def search(self, results, media, lang):
        Log("TV SEARCH CALLED")
        results.Append(MetadataSearchResult(id = 'null', score = 100))

    def update(self, metadata, media, lang):
        Log("TvUpdate. Lang %s" % lang)
        #logObject(media)
        for season in media.seasons:
            for episode in media.seasons[season].episodes:
                for item in media.seasons[season].episodes[episode].items:
                    Log("Searching xsubs for Show: %s, Season: %s, Ep: %s" % (media.title, season, episode))
                    for part in item.parts:
                        Log("Filename: %s" % os.path.basename(part.file))
                        guess = guessit(os.path.basename(part.file))
                        Log("Guess: %s" % guess)
                        if (Prefs["xsubs.username"]) and (Prefs["xsubs.password"]):
                            Log("X-Subs account credentials has been set.")
                            if not LoggedIn():
                                Log("X-Subs account is not logged in, try to Login")
                                LogIn()
                            else:
                                Log("X-Subs account is logged in")
                        else:
                            Log("X-Subs account credentials has not been set.")

                        RetrieveSeriesList()
                        if "screen_size" not in guess:
                            guess["screen_size"] = "480p"

                        episode_data = EpisodeData(media.title, season,episode, part.duration ,guess["screen_size"],guess["source"],guess["release_group"] )
                        subUrl = getSubUrl(episode_data)
                        if not subUrl:
                            Log('Subtitle URL not found')
                            return
                        Log('Subtitle URL: '+subUrl)
                        language = 'ell'
                        Log("Ready to download")
                        #subtitle = Proxy.Media(HTTP.Request(subUrl), ext='srt', format='srt')
                        subtitle = Proxy.Media(HTTP.Request(subUrl), ext='srt')
                        part.subtitles[Locale.Language.Match(language)]['xsubs'] = subtitle
                        Log("Downloaded")


