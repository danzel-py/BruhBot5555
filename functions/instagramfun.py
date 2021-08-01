from instagramy import InstagramUser
# from instagramy import InstagramPost
from requests.models import HTTPError
from replit import db

def getNewPost(uname, session_id):
    print("checking for new ig posts",uname)
    try:
        user = InstagramUser(uname,sessionid = session_id)        
        returnList = []
        posts = user.posts # dict
        
        newest = posts[0]
        # test new post here
        # db["lastIgPost"][uname] = 1
        if "lastIgPost" not in db.keys():
            db["lastIgPost"] = {}
        if uname not in db["lastIgPost"]:
            db["lastIgPost"][uname] = 0
        if db["lastIgPost"][uname] < newest.taken_at_timestamp.timestamp():
            print("yay new post")
            numOfPost = 0
            for post in posts:
                if post.taken_at_timestamp.timestamp() == db["lastIgPost"][uname]:
                    break
                numOfPost+=1
            print("we got {} new post(s)".format(numOfPost))
            db["lastIgPost"][uname] = newest.taken_at_timestamp.timestamp()
            for i in range(0,numOfPost):
                a = {'is_video': posts[i].is_video,
                    'taken_at_timestamp': posts[i].taken_at_timestamp,
                    'display_url':posts[i].display_url,
                    'post_url':posts[i].post_url
                    }
                returnList.append(a)
            return returnList
        else:
            print("no new post")
    except HTTPError:
        print("failed getting ig profile")
    except KeyError:
        return [{'post_url': "plz update sid"}]

    # except:
    #     print("some error occurred (not sid) on getting profile")

    # try:
    #     post = InstagramPost(newest.shortcode,sessionid= session_id)
    #     print(post.post_data) # dict
    # except:
    #     print("some error occurred in getting post details")
