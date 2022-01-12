import json
import time
import praw,os
import multiprocessing
import logging
import Heimdall.models as models

class PRAWCore():
    def __init__(self,auth,config):
        self.reddit_bot = praw.Reddit(**auth)
        self.inprogress = {}
        self.subreddits = self.reddit_bot.subreddit("+".join(config['subreddits']))
        save_media = config['save media']
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)
        for logger_name in ("praw", "prawcore"):
            self.logger = logging.getLogger(logger_name)
            self.logger.setLevel(logging.DEBUG)
            self.logger.addHandler(handler)
        comment_process = multiprocessing.Process(target=self.collect_comments,args=())
        submission_process = multiprocessing.Process(target=self.collect_submissions,args=())
        comment_process.start()
        submission_process.start()


    def collect_comments(self):
        for comment in self.subreddits.stream.comments(skip_existing=True):
            subproc = multiprocessing.Process(target=self.process_comment,args=(comment,))
            subproc.start()
            subproc.join()
    def collect_submissions(self):
        for submission in self.subreddits.stream.submissions(skip_existing=True):
            subproc = multiprocessing.Process(target=self.process_submission,args=(submission,))
            subproc.start()
            subproc.join()

    def process_comment(self,praw_comment):
            comment = models.getComment(praw_comment)
            if not os.path.exists(os.getcwd()+"\\"+comment['subreddit']):
                os.makedirs(os.getcwd()+"\\"+comment['subreddit'])
            if not os.path.exists(os.getcwd()+"\\"+comment['subreddit']+"\\"+comment['post_id']+".json"):
                with open(os.getcwd()+"\\"+comment['subreddit']+"\\"+comment['post_id']+".json","w+") as jsonf:
                    self.inprogress[comment['post_id']] = True
                    print(comment['post_id'])
                    submission=models.getSubmission(self.reddit_bot.submission(comment['post_id'][3:]))
                    json.dump({"post":submission,"comments":[comment]},jsonf)
                    del self.inprogress[comment['post_id']]
            else:
                with open(os.getcwd()+"\\"+comment['subreddit']+"\\"+comment['post_id']+".json","r") as jsonf:
                    if (comment['post_id'] in self.inprogress):
                       print('sleep')
                       time.sleep(15)
                    inter = json.load(jsonf)
                inter['comments'].append(comment)
                with open(os.getcwd()+"\\"+comment['subreddit']+"\\"+comment['post_id']+".json","w") as jsonf:
                    json.dump(inter,jsonf)
    def process_submission(self,praw_submission):
            submission = models.getSubmission(praw_submission)
            if not os.path.exists(os.getcwd()+"\\"+submission['subreddit']):
                os.makedirs(os.getcwd()+"\\"+submission['subreddit'])
            if not os.path.exists(os.getcwd()+"\\"+submission['subreddit']+"\\"+submission['id']+".json"):
                self.inprogress[submission['id']] = True
                with open(os.getcwd()+"\\"+submission['subreddit']+"\\"+submission['id']+".json","w+") as jsonf:
                    print(submission['id'])
                    json.dump({"post":submission,"comments":[]},jsonf)
                del self.inprogress[submission['id']]
