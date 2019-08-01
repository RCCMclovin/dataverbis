import pickle

dict_relations = { 'author': ['author', 'researcher', 'writer', 'write', 'generator', 'coauthor'],\
                   'cite': ["mention", 'quote', 'reference', 'cite'],\
                   'conference': ['conference', 'reunion','congress'],\
                   'domain' : ['domain','area', 'sphere', 'knowledge_domain', 'world', 'subject', 'topic', 'discipline', 'focus'],\
                   'journal' : ['journal', 'periodical', 'magazine', 'bulletin', 'newsletter'],\
                   'keyword' : ['keywords', 'key','topics'],\
                   'publication': ['publication', 'paper', 'issue', 'article', 'monograph', 'thesis', 'report', 'dissertation', 'essay', 'work', 'study', 'book'],\
                   'organization': ['organization', 'org', 'group', 'University']
                   }

dict_publication = { 'title' : ['name','title', 'heading'],\
                     'abstract' : ['abstract', 'wrap-up', 'summary', 'synopsis'],\
                     'citation_num' : ['citation', "citations", "number of citations"],\
                     'reference_num' : ['references'],\
                     'year': ['year', 'date'],\
                     'doi':['doi']
                     }

dict_author = { 'name': ['name', 'who'],\
                'homepage': ['homepage', 'page', 'site'],\
                'photo': ['photo', 'image']
                }

dict_conference = { 'name': ['name','what'],\
                    'full_name': ['name', 'full_name', 'what'],\
                    'homepage': ['homepage', 'page', 'site']
                    }

dict_journal = {'name': ['name','what'],\
                'full_name': ['name', 'full_name', 'what'],\
                'homepage': ['homepage', 'page', 'site']
                }

dict_organization = {'name': ['name','what'],\
                     'continent':['continent','where','location','located'],\
                     'homepage': ['homepage', 'page', 'site']
                     }

dict_domain = {'name': ['name','what', 'domain'] }

dict_cite = {'citing': ['cite', 'mention'],\
            'cited': ['cited', 'mentioned']
            }

dict_keyword = {'keyword': ['keywords','keyword', 'mention']}




outfile = open('zfiles/dict_relations','wb')
pickle.dump(dict_relations, outfile)
outfile.close()

outfile = open('zfiles/dict_publication','wb')
pickle.dump(dict_publication, outfile)
outfile.close()

outfile = open('zfiles/dict_cite','wb')
pickle.dump(dict_cite, outfile)
outfile.close()

outfile = open('zfiles/dict_keyword','wb')
pickle.dump(dict_keyword, outfile)
outfile.close()

outfile = open('zfiles/dict_domain','wb')
pickle.dump(dict_domain, outfile)
outfile.close()

outfile = open('zfiles/dict_author','wb')
pickle.dump(dict_author, outfile)
outfile.close()

outfile = open('zfiles/dict_conference','wb')
pickle.dump(dict_conference, outfile)
outfile.close()

outfile = open('zfiles/dict_journal','wb')
pickle.dump(dict_journal, outfile)
outfile.close()

outfile = open('zfiles/dict_organization','wb')
pickle.dump(dict_organization, outfile)
outfile.close()
