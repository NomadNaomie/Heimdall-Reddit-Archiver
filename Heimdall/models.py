class Comment():
    def __init__(self, author, flair, timestamp, body, post_id, op, id, parent_id, subreddit):
        self.author = author
        self.flair = flair
        self.timestamp = timestamp
        self.body = body
        self.post_id = post_id
        self.op = op
        self.id = id
        self.parent_id = parent_id
        self.subreddit = subreddit

    def json(self):
        return self.__dict__


class Submission():
    def __init__(self, author, flair, title, body, id, permalink, timestamp, author_flair, subreddit):
        self.author = author
        self.flair = flair
        self.title = title
        self.body = body
        self.id = id
        self.permalink = permalink
        self.timestamp = timestamp
        self.author_flair = author_flair
        self.subreddit = subreddit

    def json(self):
        return self.__dict__


def getSubmission(prawSubmission):
    return Submission(prawSubmission.author.name, prawSubmission.link_flair_text, prawSubmission.title,
                      prawSubmission.selftext, prawSubmission.name, prawSubmission.url, prawSubmission.created_utc,
                      prawSubmission.author_flair_text, prawSubmission.subreddit.display_name).json()


def getComment(prawComment):
    return Comment(prawComment.author.name, prawComment.author_flair_text, prawComment.created_utc, prawComment.body,
                   prawComment.link_id, prawComment.is_submitter, prawComment.name, prawComment.parent_id,
                   prawComment.subreddit.display_name).json()
