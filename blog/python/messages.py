def mail_message(post_title, post_url, name, comments):
    return f"Read {post_title} at {post_url} \n\n {name}\'s comments: {comments} "


def mail_subject(name, post_title):
    return f'{name} recommends you read {post_title}'


def mail_success_msg(post_title, to):
    return f'{post_title} was successfully sent to "{to}"'


def comment_success_save():
    return 'Your comment has been added.';
