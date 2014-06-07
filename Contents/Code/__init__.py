#xsubs.tv

import string, os, re #urllib, zipfile, copy

OS_PLEX_USERAGENT = 'plexapp.com v9.0'

seriesList = {}


resolDict = {
    '720p' : ['HDTV', 'BluRay', 'WEB-DL', 'WEBRip', 'HDDVD', 'BRRip', 'WEB-Rip'],
    '1080p' : ['BluRay', 'WEB-DL', 'WEBRip', 'WS', 'HDTV'],
    '480p' : ['HDTV', 'WEB-DL', 'BluRay', 'WEBRip'],
    '1080i' : ['HDTV'],
    '576p' : ['HDTV']
}

sourceDict = {
    'dvdrip' : ['x264', 'XviD'],
    'hdtv' : ['720p', 'XviD', 'x264', '480p', '1080i', '1080p', 'DivX', '576p'],
    'bluray' : ['720p', '1080p', '480p', 'XviD'],
    'web-dl' : ['720p', '1080p', '480p', 'x264', 'XviD', 'H264'],
    'webrip' : ['720p', '1080p', 'x264', 'XviD', '480p'],
    'pdtv' : ['HR', 'x264', 'XviD'],
    'bdrip' : ['x264', 'XviD', 'WS'],
    'tvrip' : [],
    'hddvd' : ['720p'],
    'dvdscr' : [],
    'web-rip' : ['720p'],
    'ws' : ['1080p', 'BDRip', 'XviD']
}

encDict = {
    'xvid' : ['HDTV', 'DVDRip', 'BDRip', 'WEBRip', 'WEB-DL', 'PDTV', 'AC3', 'WS', 'BluRay'],
    'x264' : ['HDTV', 'DVDRip', 'BDRip', 'WEBRip', 'WEB-DL', 'PDTV'],
    'h264' : ['WEB-DL'],
    'divx' : ['HDTV']
}

encTypesReplaceDict = {
    'dvdrip' : 'DVDRip',
    'hdtv' : 'HDTV',
    'xvid' : 'XviD',
    'x264' : 'x264',
    'bluray' : 'BluRay',
    'web-dl' : 'WEB-DL',
    'webrip' : 'WEBRip',
    'pdtv' : 'PDTV',
    'bdrip' : 'BDRip',
    'dsr' : 'DSR',
    'ws' : 'WS',
    'brrip' : 'BRRip',
    'hr' : 'HR',
    'tvrip' : 'TVRip',
    'hddvd' : 'HDDVD',
    'h264' : 'H264',
    'dvdscr' : 'DVDSCR',
    'ac3' : 'AC3',
    'divx' : 'DivX',
    'web-rip' : 'WEB-Rip'
}

#unused
encTypesDict = {
    'DVDRip' : ['x264', 'XviD'],
    '720p' : ['HDTV', 'BluRay', 'WEB-DL', 'WEBRip', 'HDDVD', 'BRRip', 'WEB-Rip'],
    'HDTV' : ['720p', 'XviD', 'x264', '480p', '1080i', '1080p', 'DivX', '576p'],
    'XviD' : ['HDTV', 'DVDRip', 'BDRip', 'WEBRip', 'WEB-DL', 'PDTV', 'AC3', 'WS', 'BluRay'],
    'x264' : ['HDTV', 'DVDRip', 'BDRip', 'WEBRip', 'WEB-DL', 'PDTV'],
    'BluRay' : ['720p', '1080p', '480p', 'XviD'],
    'WEB-DL' : ['720p', '1080p', '480p', 'x264', 'XviD', 'H264'],
    'WEBRip' : ['720p', '1080p', 'x264', 'XviD', '480p'],
    '1080p' : ['BluRay', 'WEB-DL', 'WEBRip', 'WS', 'HDTV'],
    '480p' : ['HDTV', 'WEB-DL', 'BluRay', 'WEBRip'],
    'PDTV' : ['HR', 'x264', 'XviD'],
    'BDRip' : ['x264', 'XviD', 'WS'],
    'DSR' : [],
    'WS' : ['1080p', 'BDRip', 'XviD'],
    '1080i' : ['HDTV'],
    'BRRip' : ['720p'],
    'HR' : ['PDTV'],
    'TVRip' : [],
    'HDDVD' : ['720p'],
    'H264' : ['WEB-DL'],
    'DVDSCR' : [],
    'AC3' : ['XviD'],
    'DivX' : ['HDTV'],
    'WEB-Rip' : ['720p'],
    '576p' : ['HDTV']
}

dctTeam = {}

def Start():
    HTTP.CacheTime = 0
    HTTP.Headers['User-agent'] = OS_PLEX_USERAGENT
    Log("START CALLED")

def ValidatePrefs():
    return

def getSubUrl(data):
    Log('Filename:  '+ data['sFl'])
    sre = getSourceResolutionEncoding(data['sFl'])
    fnlName = findSeriesNameinXsubs(data['sK'])
    if fnlName !='':
        srid = seriesList[fnlName]
    else:
        return

    Log(srid)
    seriesUrl = 'http://xsubs.tv/series/'+str(srid)+'/main.xml'
    Log(seriesUrl)
    elem = HTML.ElementFromURL(seriesUrl)
    subpages = elem.xpath("//series_group[@ssnnum='"+data['sTS']+"']/@ssnid")
    Log(subpages)
    Log("episode: "+data['sTE'])
    if len(subpages)==1:
        Log(data['sTS'])
        ssnUrl = 'http://xsubs.tv/series/'+str(srid)+'/'+subpages[0]+'.xml'
        ssnElem = HTML.ElementFromURL(ssnUrl)
        #First try get 
        #//subg[etitle[@number=4]]//sr[@published_on!="" and team/text()='REPACK KILLERS' and fmt/text()='HDTV.x264']//@rlsid
        fmt  = getAppropriateFmt(sre)
        Log(fmt)
        Log("//subg[etitle[@number="+data['sTE']+"]]//sr[@published_on!='' and team/text()='"+data['sR']+"' and fmt/text()='"+fmt+"']//@rlsid")
        firsttry = ssnElem.xpath("//subg[etitle[@number="+data['sTE']+"]]//sr[@published_on!='' and team/text()='"+data['sR']+"' and fmt/text()='"+fmt+"']//@rlsid")
        Log(firsttry)
        if not firsttry:
            Log(' not firsttry')
            if ('proper' in data['sFl'].lower()) or ('repack' in data['sFl'].lower()):
                #trysearch without proper or repack
                Log("if 'PROPER' or 'REPACK' in data['sFl']:")
                rlsGroup = string.replace(data['sR'], 'REPACK','')
                rlsGroup = string.replace(rlsGroup,'PROPER','').strip()
                Log(data['sFl'])
                Log(rlsGroup)
                Log("//subg[etitle[@number="+data['sTE']+"]]//sr[@published_on!='' and team/text()='"+rlsGroup+"' and fmt/text()='"+fmt+"']//@rlsid")
                secondtry = ssnElem.xpath("//subg[etitle[@number="+data['sTE']+"]]//sr[@published_on!='' and team/text()='"+rlsGroup+"' and fmt/text()='"+fmt+"']//@rlsid")
                Log(secondtry)
                if secondtry:
                    return 'http://xsubs.tv/xthru/getsub/'+ secondtry[0]
            else:
                rlsGroup = data['sR']
                rlsGroup = 'PROPER ' + rlsGroup
                Log(rlsGroup)
                Log("//subg[etitle[@number="+data['sTE']+"]]//sr[@published_on!='' and team/text()='"+rlsGroup+"' and fmt/text()='"+fmt+"']//@rlsid")
                secondtry = ssnElem.xpath("//subg[etitle[@number="+data['sTE']+"]]//sr[@published_on!='' and team/text()='"+rlsGroup+"' and fmt/text()='"+fmt+"']//@rlsid")
                Log(secondtry)
                if secondtry:
                    return 'http://xsubs.tv/xthru/getsub/'+ secondtry[0]
                rlsGroup =  string.replace(rlsGroup, 'PROPER', 'REPACK')
                Log("//subg[etitle[@number="+data['sTE']+"]]//sr[@published_on!='' and team/text()='"+rlsGroup+"' and fmt/text()='"+fmt+"']//@rlsid")
                secondtry = ssnElem.xpath("//subg[etitle[@number="+data['sTE']+"]]//sr[@published_on!='' and team/text()='"+rlsGroup+"' and fmt/text()='"+fmt+"']//@rlsid")
                Log(secondtry)
                if secondtry:
                    return 'http://xsubs.tv/xthru/getsub/'+ secondtry[0]
            Log("Not Found")
        else:
            return 'http://xsubs.tv/xthru/getsub/'+ firsttry[0]
        #xpath= //subg[etitle[@number=6]]/sr[team/text()='DIMENSION']/@rlsid
        subNode = ssnElem.xpath('//subg[etitle[@number='+data['sTE']+']]//sr[@published_on!=""]')
        Log('//subg[etitle[@number='+data['sTE']+']]//sr[@published_on!=""]')
        for lala in subNode:
            info = {}
            info['fmt'] = lala.xpath('fmt/text()')[0]
            info['hits'] = lala.xpath('hits/text()')[0]
            #//@rlsid
            info['rlsid'] = lala.xpath('./@rlsid')
            if lala.xpath('team/text()')[0] in dctTeam:
                dctTeam[lala.xpath('team/text()')[0]].append(info)
            else:
                dctTeam[lala.xpath('team/text()')[0]]= [info]
        for key, value in dctTeam.iteritems():
            Log('Key: '+key + '   Value= ')
            Log(value)
            if key.lower() == data['sR'].lower():
                for vl in value:
                    if vl['fmt'] == fmt:
                        Log("//subg[etitle[@number="+data['sTE']+"]]//sr[@published_on!='' and team/text()='"+key+"' and fmt/text()='"+fmt+"']//@rlsid")
                        secondtry = ssnElem.xpath("//subg[etitle[@number="+data['sTE']+"]]//sr[@published_on!='' and team/text()='"+key+"' and fmt/text()='"+fmt+"']//@rlsid")
                        Log(secondtry)
                        if secondtry:
                            return 'http://xsubs.tv/xthru/getsub/'+ secondtry[0]

def fillSeriesList():
    #http://xsubs.tv/series/all.xml
    seriesUrl = 'http://xsubs.tv/series/all.xml'
    elem = HTML.ElementFromURL(seriesUrl)
    subpages = elem.xpath("//series")
    for l in subpages:
        seriesList[l.xpath('./text()')[0]] = int(l.xpath('./@srsid')[0])

def getReleaseGroup(filename):
    tmpFile = string.replace(filename, '-', '.')
    splitName = string.split(tmpFile, '.')
    if ('gttvsd' in splitName[-2].lower()) or ('gtrd'in splitName[-2].lower()) or ('eztv'in splitName[-2].lower()) or ('vtv'in splitName[-2].lower()):
        group = splitName[-3].strip()
    else:
        group = splitName[-2].strip() 
    if 'REPACK' in filename:
        group = 'REPACK '+ group
    if 'PROPER' in filename:
        group = 'PROPER ' + group
    Log("group= " + group)
    return group

def getSourceResolutionEncoding(filename):
    tmpFile = filename.lower()
    splitName = string.split(tmpFile, '.')
    retval = {'Source' : '','Resolution' : '','Encoding' : ''}
    for l in splitName:
        if l in sourceDict:
            Log("Source in SourceDict: " + l)
            retval['Source'] = encTypesReplaceDict[l]
        if l in resolDict:
            retval['Resolution'] = l
        if l in encDict:
            retval['Encoding'] = encTypesReplaceDict[l]
    if retval['Encoding'] == '':
        if '264' in tmpFile:
            retval['Encoding'] = 'x264'
        else:
            Log("if '264' in tmpFile: = FALSE")
            tmpFile = string.replace(filename.lower(), '-', '.')
            splitName = string.split(tmpFile, '.')
            for l in splitName:
                if l in encDict:
                    retval['Encoding'] = encTypesReplaceDict[l]
    if retval['Source'] == '':
        Log("if retval['Source'] == '':")
        tmpFile = string.replace(filename.lower(), '-', '.')
        splitName = string.split(tmpFile, '.')
        for l in splitName:
            if l in sourceDict:
                retval['Source'] = encTypesReplaceDict[l]
    if retval['Resolution'] == '':
        Log("if retval['Resolution'] == '':")
        tmpFile = string.replace(filename.lower(), '-', '.')
        splitName = string.split(tmpFile, '.')
        for l in splitName:
            if l in resolDict:
                retval['Resolution'] = encTypesReplaceDict[l]
    Log("Source: %s" % retval['Source'])
    Log("Resolution: %s" % retval['Resolution'])
    Log("Encoding: %s" % retval['Encoding'])
    return retval

#according to xsubs site
def getAppropriateFmt(fmtValues):
    retval = ''
    if fmtValues['Resolution'] != '':
        retval = fmtValues['Resolution'] + '.' + fmtValues['Source']
        Log("Fmt value: %s" % retval)
        return retval
    else:
        if fmtValues['Source']!= '' and fmtValues['Encoding'] != '':
            retval = fmtValues['Source'] + '.' + fmtValues['Encoding']
            Log("Fmt value: %s" % retval)
            return retval
        if fmtValues['Source']== '':
            retval =  fmtValues['Encoding']
            Log("Fmt value: %s" % retval)
            return retval
        else:
            retval =  fmtValues['Source']
            Log("Fmt value: %s" % retval)
            return retval
    Log("Fmt value: %s" % retval)
    return retval

def findSeriesNameinXsubs(name):
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
        Log('1 Original name: ' + name + '    found name: ' + fnlName)
        return fnlName
    for key, value in seriesList.iteritems():
        if re.sub(r'\[[^)]*\]', '', key).lower().strip() == fnlName.lower():
            Log('2 Original name: ' + name + '    found name: ' + key)
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
        Log('3 Original name: ' + name + '    found name: ' + hgName)
        return hgName
    return ''





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
        for season in media.seasons:
            for episode in media.seasons[season].episodes:
                for item in media.seasons[season].episodes[episode].items:
                    Log("show: %s" % media.title)
                    Log("Season: %s, Ep: %s" % (season, episode))
                    for part in item.parts:
                        Log("Release group: %s" % getReleaseGroup(part.file))
                        data = {}
                        data['sK'] = media.title
                        data['sTS'] = season
                        data['sTE'] = episode
                        data['sR'] = getReleaseGroup(part.file)
                        data['sFl'] = part.file

                        fillSeriesList()

                        subUrl = getSubUrl(data)
                        if not subUrl:
                            Log('Subtitle URL not found')
                            return
                        Log('Subtitle URL: '+subUrl)
                        language = 'ell'
                        
                        if language in part.subtitles:
                            if subUrl in part.subtitles[language]:
                                return
                        Log("ready to download")
                        Log(language)

                        part.subtitles[Locale.Language.Match(language)][subUrl+'xsubs'] = Proxy.Media(HTTP.Request(subUrl), codec='srt', format='xsubs.srt')


