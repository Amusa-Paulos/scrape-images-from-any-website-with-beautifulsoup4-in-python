import requests, sys
from bs4 import BeautifulSoup

# https://unsplash.com/s/photos/cat
print("Parsing query...")
query = ' '.join(sys.argv[1:])
print("Query parsed")

m_lnk = lambda link: link.get('src').split('?')[0]

print(f"requesting Unsplash.com for {query} pictures...")
req = requests.get(f'https://unsplash.com/s/photos/{query}')
req.raise_for_status()
print("Done requesting!")

print("Parsing HTML response content...")
soup = BeautifulSoup(req.text)
print("HTML response content parsed")

print("finding all search result img elements...")
imgs_els = soup.find_all(attrs={'data-test': "photo-grid-masonry-img"})
print("all search result img elements found and grouped")
# print(imgs_els[0].get('src'))

srcLinks = []

print("Filtering image links from img elements")
[srcLinks.append(m_lnk(link)) if m_lnk(link) not in srcLinks else None for link in imgs_els]
print("image links from img elements filtered")

print("Downloading images...")
for link in srcLinks:
    print(f"Downloading {link}...")

    print('scraping image...')
    img_req = requests.get(link)
    img_req.raise_for_status()
    print('image scraped')

    print('Parsing image...')
    file_ext = img_req.headers['Content-Type'].split('/')[-1] # image/jpeg
    file_name = link.split('/')[-1] + "." + file_ext
    print('Image parsed')

    print(f'Writing {file_name}...')
    with open(file_name, 'wb') as _fl:
        for chunk in img_req.iter_content(100000):
            _fl.write(chunk)
    print(f"{file_name} written successfully!")

print("Done!")
    
    
