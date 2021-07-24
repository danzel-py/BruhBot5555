from instagramy import InstagramUser,InstagramPost
from requests.models import HTTPError
from replit import db

def getNewPost(uname, session_id):
    print("checking for new ig posts",uname)
    try:
        user = InstagramUser(uname,sessionid = session_id)        
            
        posts = user.posts # dict
        
        newest = posts[0]
        # test new post here
        # db["lastIgPost"] = 1
        if "lastIgPost" not in db.keys():
            db["lastIgPost"] = newest.taken_at_timestamp.timestamp()
        else:
            if db["lastIgPost"] < newest.taken_at_timestamp.timestamp():
                print("yay new post")
                db["lastIgPost"] = newest.taken_at_timestamp.timestamp()
                return {'is_video': newest.is_video,
                'taken_at_timestamp': newest.taken_at_timestamp,
                'display_url':newest.display_url,
                'post_url':newest.post_url
                }
            else:
                print("no new post")
    except HTTPError:
        print("failed getting ig profile")
    # except:
    #     print("some error occurred (not sid) on getting profile")

    # try:
    #     post = InstagramPost(newest.shortcode,sessionid= session_id)
    #     print(post.post_data) # dict
    # except:
    #     print("some error occurred in getting post details")
