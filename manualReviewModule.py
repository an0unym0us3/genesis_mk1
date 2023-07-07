class User:
    def __init__(self, userid, user_locale, user_score):
        self.id = userid
        self.loc = user_locale
        self.score = user_score


class Website:
    def __init__(self, website_domain):
        self.dom = website_domain
        self.review = dict()
        self.score = 0

    def update_review(self, the_user, the_review=None):
        # if there was no input to the review, then it is understood that the review of the user must be deleted
        if the_review is None:
            # The score will be the original total score - the users score, divided by the new total (which is one less)
            self.score = (self.score * len(self.review) - self.review[the_user][1]) / (len(self.review) - 1)
            del self.review[the_user]
        else:
            # try to get the old review of the user
            try:
                old_score = self.review[the_user][1]
                # the total number of reviews is the same, but the difference between the old and new is adjusted
                self.score =(self.score * (len(self.review)) + the_review[1] - old_score) / len(self.review)
            # if the old review doesn't exist then create a new one
            except KeyError:
                # just add it to the total sum and divide accounting for 1 more review, which is this one
                self.score =(self.score * (len(self.review)) + the_review[1]) / (len(self.review)+1)
            # actually record the review
            self.review[the_user] = the_review


amazon = Website('https://www.amazon.com/')

amazon.update_review('e', ['This is only for testing purposes and is the first review', 7])
amazon.update_review('f', ['This is only for testing purposes and is the first review', 9])
amazon.update_review('g', ['This is only for testing purposes and is the first review', 40])
amazon.update_review('h', ['This is only for testing purposes and is the first review', 31])
amazon.update_review('i', ['This is only for testing purposes and is the first review', 69])
amazon.update_review('i')
amazon.update_review('g', ['This is only for testing purposes and is the first review', 45])

print(amazon.score)
