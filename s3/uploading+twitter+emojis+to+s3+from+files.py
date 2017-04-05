import boto3
import cairosvg

#Verify permissions are working
s3 = boto3.resource('s3')
for bucket in s3.buckets.all():
    print(bucket.name)

#read in a file of emoji names
with open('data/emoji_numbers_76.txt') as f:
    content = f.readlines()
#remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content]

client = boto3.client('s3')
for _ in range(len(content)):
    emoji = content[_]
    emoji_file = 'twitter-emojis/svg-all/' + emoji + '.svg'
    emoji_png_file = emoji +  '.png'
    image = cairosvg.svg2png(file_obj = open(emoji_file, "rb"), scale = 2)
    response = client.put_object(
        ACL='public-read',
        Body=image,
        Bucket='gentle-persuader-emoji',
        Key=emoji_png_file
        )

#verify upload
for bucket in s3.buckets.all():
    for key in bucket.objects.all():
        print(key.key)
