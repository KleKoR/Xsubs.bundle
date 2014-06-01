#xsubs.tv

import string, os, urllib, zipfile, re, copy

OS_PLEX_USERAGENT = 'plexapp.com v9.0'

series = {
    '100 Questions': 276,
    '100 (The)': 561,
    '2 Broke Girls': 158,
    '24': 4,
    '30 Rock': 29,
    '37 Days': 574,
    '4400 (The)': 90,
    '666 Park Avenue': 420,
    '7.39 (The)': 539,
    '90210': 30,
    '100 Greatest Discoveries': 319,
    '1066': 404,
    'About a Boy': 554,
    'Adventures of Tintin (The)': 419,
    'Afro Samurai': 318,
    'After (The)': 559,
    'Alcatraz': 140,
    'Alias': 45,
    'Alice': 403,
    'Aliens in America': 249,
    'Almost Human': 528,
    'Alphas': 183,
    'American Dad!': 31,
    'American Gothic': 352,
    'American Horror Story': 187,
    'Americans (The) [2013]': 523,
    'Angel': 64,
    'Anger Management': 421,
    'Ani-Kuri 15': 505,
    'Aquaman': 418,
    'Archer [2009]': 535,
    'Arrested Development': 91,
    'Arrow': 422,
    'Assassin\'s Creed': 385,
    'Atlantis [2013]': 520,
    'Avatar: the Last Airbender': 239,
    'Avengers Assemble': 477,
    'Avengers: Earth\'s Mightiest Heroes (The)': 452,
    'Awake': 204,
    'Apocalypse: Second World War': 296,
    'America\'s Next Top Model': 358,
    'Babylon 5': 81,
    'Back to You': 402,
    'Bag of Bones': 357,
    'Band of Brothers': 308,
    'Banshee': 450,
    'Barco (El)': 432,
    'Batman (The)': 531,
    'Battlestar Galactica': 20,
    'Battlestar Galactica [1978]': 238,
    'Beast (The)': 295,
    'Beauty and the Beast': 132,
    'Beauty and the Beast [2012]': 512,
    'Being Erica': 172,
    'Being Human [2008]': 194,
    'Believe': 557,
    'Betrayal': 526,
    'Better with You': 300,
    'Beverly Hills 90210': 26,
    'Big Bang Theory (The)': 14,
    'Big C (The)': 139,
    'Big Shots': 294,
    'Big Time Rush': 474,
    'Bionic Woman': 253,
    'Birds of Prey': 293,
    'Black Books': 401,
    'Black Donnellys (The)': 400,
    'Black Mirror': 333,
    'Black Sails': 544,
    'Blackadder': 213,
    'Blacklist (The)': 506,
    'Blackstar': 543,
    'Blade: the Series [2006]': 278,
    'Blood Ties': 292,
    'Blue Bloods': 307,
    'Body of Proof': 89,
    'Bones': 57,
    'Bonnie & Clyde': 532,
    'Bored to Death': 317,
    'Borgias (The)': 129,
    'Boston Legal': 69,
    'Bravestarr': 441,
    'Breaking Bad': 73,
    'Breaking In': 291,
    'Bridge (The)': 484,
    'Bron|Broen': 509,
    'Brooklyn Nine-Nine': 519,
    'Brothers and Sisters': 52,
    'Buffy the Vampire Slayer': 44,
    'Bullet in the Face': 438,
    'Burn Notice': 53,
    'Californication': 41,
    'Call the Midwife': 454,
    'Camelot': 237,
    'Cape (The) [2011]': 175,
    'Caprica': 186,
    'Carnivΰle': 128,
    'Carrie Diaries (The)': 469,
    'Cashmere Mafia': 299,
    'Castle [2009]': 265,
    'Ch:os:en': 479,
    'Charmed': 55,
    'Chicago Fire': 496,
    'Chuck': 25,
    'Class (The)': 371,
    'Cleveland Show (The)': 61,
    'Cold Case': 118,
    'Combat Hospital': 290,
    'Come Fly With Me': 342,
    'Committed': 370,
    'Complete Savages': 261,
    'Continuum': 423,
    'Continuum Web Series': 553,
    'Copper': 424,
    'Corner (The)': 399,
    'Cougar Town': 163,
    'Count Duckula': 152,
    'Coupling [2000]': 351,
    'Crazy Ones (The)': 511,
    'Criminal Minds': 126,
    'Criminal Minds: Suspect Behavior': 384,
    'Crimson Field (The)': 577,
    'Crisis': 560,
    'Crossing Lines': 485,
    'Crusade': 212,
    'CSI: Las Vegas': 16,
    'CSI: Miami': 34,
    'CSI: New York': 21,
    'Cult': 449,
    'Cupid [2009]': 264,
    'Curb Your Enthusiasm': 289,
    'Cosmos: A Space-Time Odyssey': 558,
    'Da Vinci\'s Demons': 463,
    'Dallas [2012]': 570,
    'Damages': 62,
    'Dancing on the Edge': 565,
    'Dark Angel': 168,
    'Darkwing Duck': 84,
    'Dawson\'s Creek': 117,
    'Day Break': 369,
    'Dead Like Me': 236,
    'Dead Zone (The)': 72,
    'Deadwood': 157,
    'Death Comes to Pemberley': 533,
    'Deception': 442,
    'Defiance': 465,
    'Defying Gravity': 288,
    'Desperate Housewives': 10,
    'Devious Maids': 492,
    'Dexter': 17,
    'Diary of Anne Frank (The)': 368,
    'Dirt': 245,
    'Dirty Sexy Money': 167,
    'Divine: the Series': 482,
    'Do Not Disturb': 383,
    'Doctor Who [2005]': 78,
    'Dollhouse': 85,
    'Downton Abbey': 124,
    'Dr Horrible\'s Sing-along Blog': 350,
    'Dracula': 507,
    'Dragon Ball': 6,
    'Dragon Ball Z': 19,
    'Drake and Josh': 332,
    'Dresden Files (The)': 275,
    'Drifters': 527,
    'Drive': 398,
    'Duck Tales': 110,
    'Early Edition': 466,
    'Earth 2': 230,
    'Eastbound & Down': 155,
    'Elementary': 437,
    'Eleventh Hour [2008]': 174,
    'Eli Stone': 131,
    'Enlisted': 538,
    'Entourage': 35,
    'Episodes': 221,
    'ER': 224,
    'Escape Artist (The)': 563,
    'Eureka': 100,
    'Event (The)': 115,
    'Everwood': 331,
    'Everybody Loves Raymond': 106,
    'Extras': 263,
    'Earth: the Power of the Planet': 298,
    'Fades (The)': 316,
    'Fairly Legal': 330,
    'Fall (The)': 470,
    'Fallen': 416,
    'Falling Skies': 189,
    'Family Guy': 11,
    'Fargo': 569,
    'Farscape': 93,
    'Fawlty Towers': 287,
    'Fear Itself': 193,
    'Femme Nikita (La)': 105,
    'Firefly': 200,
    'Firm (The)': 297,
    'Flash (The)': 341,
    'Flashforward': 149,
    'Fleming: the Man Who Would Be Bond': 551,
    'Flight of the Conchords': 137,
    'Following (The)': 445,
    'Fosters (The)': 493,
    'Freaks and Geeks': 252,
    'Free Agents [2011]': 367,
    'Fresh Prince of Belair (The)': 215,
    'Friday Night Lights': 59,
    'Friday the 13th: the Series': 113,
    'Friends': 32,
    'Friends with Better Lives': 568,
    'Fringe': 12,
    'From Dusk Till Dawn': 562,
    'Futurama': 51,
    'From the Earth to the Moon': 286,
    'Galactica [1980]': 244,
    'Game of Thrones': 101,
    'Ghost Squad (The)': 329,
    'Ghost Whisperer': 42,
    'Ghostfacers [2010]': 306,
    'Gilmore Girls': 86,
    'Glades (The)': 145,
    'Glee': 68,
    'Golan the Insatiable': 547,
    'Good Wife (The)': 259,
    'Goodwin Games (The)': 473,
    'Gossip Girl': 38,
    'Graceland': 481,
    'Great Expectations [2011]': 529,
    'Greek': 98,
    'Grey\'s Anatomy': 13,
    'Grimm': 142,
    'Galapagos Islands': 382,
    'Genius of Charles Darwin (The)': 489,
    'H+': 447,
    'Halo 4: Forward unto Dawn': 471,
    'Hannibal': 459,
    'Happy Town': 397,
    'Harper\'s Island': 169,
    'Hart of Dixie': 181,
    'Haven': 87,
    'Hawaii Five-0': 54,
    'Helix': 534,
    'Hell on Wheels': 208,
    'Hellcats': 199,
    'Hemlock Grove': 464,
    'Hercules: the Legendary Journeys': 396,
    'Heroes': 22,
    'Hidden': 340,
    'Highlander': 180,
    'Highlander: the Raven': 395,
    'Hit & Miss': 478,
    'Hit the Floor': 498,
    'Homeland': 220,
    'House of Cards [2013]': 476,
    'House, MD': 8,
    'How I Met Your Mother': 9,
    'Hulk and the Agents of SMASH': 504,
    'Hung': 80,
    'Hunted': 425,
    'Hustle': 138,
    'How Earth Made Us': 258,
    'How the Earth Was Made': 339,
    'I Dream of Jeannie': 257,
    'In Plain Sight': 366,
    'In the Flesh': 461,
    'In Treatment': 109,
    'Increasingly Poor Decisions of Todd Margaret (The)': 305,
    'Intelligence [2014]': 536,
    'Internado (El)': 102,
    'Invasion': 154,
    'IT Crowd (The)': 136,
    'It\'s Always Sunny in Philadelphia': 47,
    'In the Shadow of the Moon': 415,
    'Incredible Human Journey (The)': 315,
    'Jane Eyre': 365,
    'Jeff Dunham Show (The)': 274,
    'Jericho': 88,
    'Joan of Arcadia': 248,
    'Job (The)': 328,
    'Joey': 92,
    'John Adams': 235,
    'Journeyman': 198,
    'Just Shoot Me': 285,
    'Justice League': 95,
    'K-Ville': 349,
    'Kennedys (The)': 219,
    'Killing (The)': 148,
    'Killpoint (The)': 284,
    'King [2011]': 381,
    'Kingdom Hospital': 203,
    'Kitchen Confidential': 283,
    'Klondike [2014]': 537,
    'Knight Rider [1982]': 166,
    'Knight Rider [2008]': 141,
    'Kuzey Gόney': 521,
    'Kyle XY': 114,
    'L Word (The)': 108,
    'LAPD': 414,
    'Las Vegas': 147,
    'Last Days of Pompeii (The)': 440,
    'Last Templar (The)': 327,
    'Law & Order: UK': 273,
    'Law & Order: Criminal Intent': 356,
    'Law & Order: Special Victims Unit': 46,
    'League (The)': 272,
    'League of Gentlemen (The)': 412,
    'Legend of the Seeker': 150,
    'Lie to Me': 56,
    'Life [2007]': 411,
    'Life After People': 394,
    'Life on Mars': 260,
    'Life\'s Too Short': 314,
    'Line of Duty': 426,
    'Listener (The)': 326,
    'Little Britain': 211,
    'Little Britain USA': 282,
    'Lois & Clark: the New Adventures of Superman': 234,
    'Loonatics Unleashed': 348,
    'Looney Tunes': 380,
    'Lost': 2,
    'Lost Girl': 451,
    'Lost Room (The)': 313,
    'Louie': 188,
    'Last Day of the Dinosaurs': 413,
    'MacGyver': 99,
    'Mad Love': 202,
    'Mad Men': 71,
    'Marchlands': 542,
    'Married with Children': 135,
    'Marvel\'s Agents of SHIELD': 501,
    'Masters of Horror': 182,
    'Masters of Science Fiction': 281,
    'Masters of Sex': 510,
    'Matroesjka\'s': 516,
    'McLaren Tooned': 499,
    'Medium': 171,
    'Melrose Place': 162,
    'Mentalist (The)': 70,
    'Merlin [2008]': 123,
    'Metalocalypse': 347,
    'Miami Vice': 229,
    'Mighty Morphine Power Rangers': 218,
    'Mike & Molly': 393,
    'Mill (The)': 550,
    'Millenium [1996]': 228,
    'Miss/Guided': 325,
    'Missing [2012]': 324,
    'Mistresses [2013]': 472,
    'Mob City': 530,
    'Modern Family': 75,
    'Mom': 518,
    'Monk': 243,
    'Moonlight': 185,
    'Mortal Kombat: Conquest': 134,
    'Mortal Kombat: Legacy': 111,
    'Motive': 552,
    'Mr Bean': 262,
    'Mr Bean: The Animated Series': 566,
    'Mr Sunshine': 280,
    'Mrs Brown\'s Boys': 217,
    'My Babysitter\'s a Vampire': 379,
    'My Name Is Earl': 43,
    'Nanny (The)': 227,
    'Naruto': 355,
    'Neighbors (The)': 525,
    'Neighbors from Hell': 346,
    'Neverland': 364,
    'New Girl': 312,
    'Nightmares & Dreamscapes': 242,
    'Nikita': 144,
    'Nip/Tuck': 50,
    'North & South [1985]': 345,
    'North Shore': 304,
    'Numb3rs': 28,
    'Nurse Jackie': 122,
    'NYPD Blue': 165,
    'Nature\'s Great Events': 251,
    'OC (The)': 49,
    'Office (The) [2001]': 271,
    'Office (The) [2005]': 410,
    'Once Upon a Time [2011]': 125,
    'One Tree Hill': 15,
    'Orange is the New Black': 488,
    'Originals (The)': 490,
    'Orphan Black': 486,
    'Outcasts': 303,
    'Outer Limits (The)': 311,
    'OZ': 270,
    'Origins of Us': 277,
    'Pacific (The)': 161,
    'Pan Am': 192,
    'Parade\'s End': 427,
    'Paradise (The)': 517,
    'Paranoia Agent': 497,
    'Parks and Recreation': 65,
    'Party Down': 250,
    'Peaky Blinders': 502,
    'Penguins of Madagascar (The)': 133,
    'Penny Dreadful': 573,
    'Perception': 428,
    'Person of Interest': 160,
    'Persona 4': 191,
    'PG Porn': 310,
    'Planet of the Apes (The)': 363,
    'Poirot [1989]': 309,
    'Poison Tree (The)': 458,
    'Pokιmon': 216,
    'Pretty Little Liars': 127,
    'Primeval': 143,
    'Primeval New World': 429,
    'Prison Break': 24,
    'Prisoner (The)': 201,
    'Private Practice [2007]': 279,
    'Psychoville': 197,
    'Pushing Daisies': 159,
    'Planet Earth': 247,
    'Rabbids Invasion': 495,
    'Raines': 392,
    'Raising Hope': 269,
    'Ravenswood': 514,
    'Ray Donovan': 487,
    'Reaper': 130,
    'Rectify': 468,
    'Red Road (The)': 555,
    'Red Widow': 456,
    'ReGenesis': 226,
    'Reign': 540,
    'Rescue Me': 323,
    'Resurrection [2014]': 556,
    'Return of Jezebel James (The)': 391,
    'Revenants (Les)': 575,
    'Revenge': 146,
    'Revolution [2012]': 430,
    'Ring of Fire': 455,
    'Ringer': 156,
    'Ripper Street': 435,
    'Rizzoli & Isles': 475,
    'Robot Chicken': 354,
    'Rome': 104,
    'Roommates': 246,
    'Rosemary\'s Baby': 572,
    'Roswell': 121,
    'Royal Pains': 210,
    'Rubicon': 207,
    'Rules of Engagement': 196,
    'Real White Queen and Her Rivals (The)': 494,
    'Salem': 567,
    'Samantha Who': 409,
    'Samurai Jack': 467,
    'Sanctuary [2008]': 390,
    'Sarah Connor Chronicles (The)': 83,
    'Scandal [2012]': 443,
    'School of Thrones': 462,
    'Scrubs': 256,
    'SeaQuest DSV': 431,
    'Secret Circle (The)': 120,
    'Secret Diary of a Call Girl': 408,
    'Secret Life of the American Teenager (The)': 344,
    'Secret State': 433,
    'Seinfeld': 18,
    'Seth MacFarlane\'s Cavalcade of Cartoon Comedy': 338,
    'Sex and the City': 40,
    'Shark': 103,
    'Sherlock [2010]': 178,
    'Shield (The)': 37,
    'Shit! My Dad Says': 206,
    'Simpsons (The)': 1,
    'Sinbad': 439,
    'Single Father': 491,
    'Six Feet Under': 97,
    'Sledgehammer': 225,
    'Sleeper Cell': 302,
    'Sleepy Hollow': 503,
    'Smallville': 3,
    'Smash': 378,
    'Sons of Anarchy': 58,
    'Sons of Tucson': 337,
    'Sopranos (The)': 77,
    'South of Nowhere': 377,
    'South Park': 5,
    'Southland': 268,
    'Space 1999': 153,
    'Spartacus [2010]': 74,
    'Spooks': 233,
    'Star Trek [TOS]': 67,
    'Star Trek: Deep Space Nine': 336,
    'Star Trek: Enterprise': 170,
    'Star Trek: the Next Generation': 48,
    'Star Trek: Voyager': 353,
    'Star Wars: Clone Wars [2003]': 389,
    'Star Wars: Clone Wars [2008]': 388,
    'Star-Crossed': 549,
    'Stargate: Atlantis': 27,
    'Stargate: SG-1': 79,
    'Street Fighter II: V': 267,
    'Street Fighter: Assassin\'s Fist': 576,
    'Studio 60 on the Sunset Strip': 223,
    'Super Fun Night': 513,
    'Superman Classic Cartoons': 177,
    'Supernatural': 7,
    'Supernatural: the Animation': 195,
    'Surface': 255,
    'Taken [2002]': 301,
    'Tales from the Crypt': 82,
    'Teen Titans': 376,
    'Teen Wolf [2011]': 444,
    'Terra Nova': 176,
    'Terry Pratchett\'s the Colour of Magic [2008]': 387,
    'That 70\'s Show': 407,
    'Thin Blue Line (The)': 362,
    'Threshold': 361,
    'Thundercats': 66,
    'Til Death': 322,
    'Tin Man': 375,
    'Tom and Jerry Show (The)': 571,
    'Tomorrow People (The)': 515,
    'Top of the Lake': 460,
    'Torchwood': 209,
    'Touch [2012]': 254,
    'Town (The)': 436,
    'Traveler': 241,
    'Treme': 184,
    'Triangle (The)': 374,
    'Tru Calling': 373,
    'True Blood': 36,
    'True Detective': 541,
    'Tudors (The)': 107,
    'Tunnel (The)': 522,
    'Twin Peaks': 173,
    'Two and a Half Men': 23,
    'Two Guys and a Girl': 360,
    'Top Gear': 406,
    'Ugly Betty': 214,
    'Ultimate Spider-Man': 434,
    'Under the Dome': 480,
    'Unit (The)': 222,
    'United States of Tara': 386,
    'Universe (The)': 94,
    'Utopia': 446,
    'V [2009]': 119,
    'Vampire Diaries (The)': 33,
    'Vanished': 240,
    'Veronica Mars': 60,
    'Victorious': 321,
    'Vikings': 453,
    'Walking Dead (The)': 76,
    'Warehouse 13': 546,
    'Web Therapy': 232,
    'Weeds': 63,
    'West Wing': 96,
    'What Remains': 524,
    'White Queen (The)': 483,
    'Whitechapel': 205,
    'Widower (The)': 564,
    'Wilfred': 545,
    'Wilfred [2011]': 190,
    'Wire (The)': 151,
    'Witches of East End': 508,
    'Without a Trace': 112,
    'Women\'s Murder Club': 343,
    'Wonder Years (The)': 405,
    'Woodley': 548,
    'Worst Week': 231,
    'X-Files (The)': 39,
    'X-Men: the Animated Series': 320,
    'Xena Warrior Princess': 164,
    'XIII: the Series': 457,
    'XIII: the Conspiracy': 335,
    'Yes Minister': 334,
    'Young Indiana Jones Chronicles (The)': 372,
    'Young Justice': 116,
    'Yu-Gi-Oh!': 266,
    'Zero Hour [2013]': 448,
    'Zorro [1957]': 359
}

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
        srid = series[fnlName]
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
    if fnlName in series:
        Log('1 Original name: ' + name + '    found name: ' + fnlName)
        return fnlName
    for key, value in series.iteritems():
        if re.sub(r'\[[^)]*\]', '', key).lower().strip() == fnlName.lower():
            Log('2 Original name: ' + name + '    found name: ' + key)
            return key


    tmpDict = {}
    splName  = string.split(name,' ')
    for key, value in series.iteritems():
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


