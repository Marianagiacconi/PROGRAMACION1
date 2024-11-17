# returns True if number is even
def reviewFilters(request, ReviewModel, reviews):
    if request.get_json():
        filters = request.get_json().items()
        for key, value in filters:
            if key == 'byScore[gt]':
                reviews = reviews.filter(ReviewModel.score > float(value))
            if key == 'byScore[lte]':
                reviews = reviews.filter(ReviewModel.score < float(value))
            if key == 'byUserID':
                reviews = reviews.filter(ReviewModel.userID == str(value))
    return reviews

def poemFilters(request, PoemsModel, poems):
    if request.get_json():
        filters = request.get_json().items()
        for key, value in filters:
            if key == 'byTitle':
                poems = poems.filter(PoemsModel.title == str(value))
            if key == 'byUserId':
                poems = poems.filter(PoemsModel.userID == int(value))
    return poems

def userFilters(request, UserModel, users):
    if request.get_json():
        filters = request.get_json().items()
        for key, value in filters:
            if key == 'byName':
                users = users.filter(UserModel.firstname == str(value))
            if key == "order_by":
                if value == "firstname[desc]":
                    users = users.order_by(UserModel.firstname.desc())
                if value == "firstname":
                    users = users.order_by(UserModel.firstname)
    return users