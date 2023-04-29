from flask import Flask, request
import musicbrainzngs

app = Flask(__name__)

musicbrainzngs.set_useragent('Album Cover Search', 'version', contact=None)

@app.route('/api/album-cover')
def get_album_cover():
    artist = request.args.get('artist')
    album = request.args.get('album')
    images = []

    try:
        release_groups = musicbrainzngs.search_release_groups(artist=artist, release=album, limit=5)['release-group-list']
    except musicbrainzngs.ResponseError as e:
        print(f'Request failed with error: {e}')
        return 'No results!'
    else:
        for release_group in release_groups:
            try:
                images_list = musicbrainzngs.get_release_group_image_list(release_group['id'])['images']
            except musicbrainzngs.ResponseError as e:
                print(f'Request failed with error: {e}')
            else:
                if(len(images_list) == 0):
                    return 'No results!'
                else:
                    for i in range(min(len(images_list), 3)):
                        images.append(images_list[i]['image'])

    return images

if __name__ == '__main__':
    app.run()