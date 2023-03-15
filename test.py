import requests
import csv

# Facebook Page ID and Access Token
page_id = "1491118234437160"
access_token = "EAAICZA8nky80BABNqn6RD2SJzg9IG0T9GmmHQNnX179kOKzsZBDlKXojFtG5HhfkcX9hxj0NRtUHuJch0BNUrEipnrltmVJJS1OZA4kZCX3rgpRzI2fuCLgAOPBv6TPGvj1r1LpjdiZCUrqmZAn7qG3OHKfJPyyHd7jvssrNCh1K89YFYnNfL4wBOLwZAMPirYxQEdKgtxqsRJIXZCAneS8K"

# API endpoint for getting page posts
url = f"https://graph.facebook.com/v12.0/{page_id}/posts?access_token={access_token}"

# Create a CSV file to store user data
user_csv_file = open('user_data.csv', 'w', newline='')
user_csv_writer = csv.writer(user_csv_file)

# Write header row to user CSV file
user_csv_writer.writerow(['User ID', 'User Name', 'User Profile URL', 'Interaction Type', 'Interaction Time'])
# Create a CSV file to store post data
post_csv_file = open('post_data.csv', 'w', newline='')
post_csv_writer = csv.writer(post_csv_file)

# Write header row to post CSV file
post_csv_writer.writerow(['Post ID', 'Message', 'Link', 'Type', 'Created Time'])

# Fetch data from the Facebook page
while url:
    # Get the page posts
    response = requests.get(url)
    data = response.json()
    
    # Check if there are no more posts
    if 'data' not in data:
        break
        
    # Loop through each post and write post data to CSV file
    for post in data['data']:
        post_csv_writer.writerow([post['id'], post.get('message', ''), post.get('link', ''), post['type'], post['created_time']])
        
        # API endpoint for getting post reactions
        reactions_url = f"https://graph.facebook.com/v12.0/{post['id']}/reactions?access_token={access_token}"
        
        # Get reactions data
        reactions_response = requests.get(reactions_url)
        reactions_data = reactions_response.json()
        
        # Loop through each reaction and write user data to CSV file
        for reaction in reactions_data['data']:
            user_csv_writer.writerow([reaction['id'], reaction['name'], f"https://www.facebook.com/{reaction['id']}", "Reaction", reaction['created_time']])
            
        # API endpoint for getting post comments
        comments_url = f"https://graph.facebook.com/v12.0/{post['id']}/comments?access_token={access_token}"
        
        # Get comments data
        comments_response = requests.get(comments_url)
        comments_data = comments_response.json()
        
        # Loop through each comment and write user data to CSV file
        for comment in comments_data['data']:
            user_csv_writer.writerow([comment['from']['id'], comment['from']['name'], f"https://www.facebook.com/{comment['from']['id']}", "Comment", comment['created_time']])
    
    # Get the next page of posts
    url = data['paging'].get('next')

# Close the CSV files
user_csv_file.close()
post_csv_file.close()

