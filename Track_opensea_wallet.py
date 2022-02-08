from selenium import webdriver
from bs4 import BeautifulSoup
import random
import os
import time

# Function To efficiently search throw html document, to use lest repetitive code
def search(tag, clasa, cont):
    line_content = cont.find_all(tag, class_=clasa)
    if len(line_content) > 0:
        line_content = line_content[len(line_content) - 1]
    return line_content

def execute(wallet_owner):
    with open("opensea_html.txt", "r+") as f:
        previous_action = f.read()

    os.environ["PATH"] = r"C:/browsers_drivers/geckodriver-v0.30.0-win64"

    # Instantiating a web browser session to visit Opensea website and scroll down the page to get loaded data
    driver = webdriver.Firefox()
    driver.maximize_window()
    url = f"https://opensea.io/{wallet_owner}?tab=activity&search[chains][0]=ETHEREUM&search[eventTypes][0]=AUCTION_SUCCESSFUL&search[eventTypes][1]=AUCTION_CREATED"
    driver.get(url)
    time.sleep(random.randint(4, 5))
    driver.execute_script("window.scrollTo(0, 330)")
    time.sleep(random.randint(4, 6))

    # Getting the Html document from Opensea website and closing the browser instance
    html = driver.page_source
    content = BeautifulSoup(html, 'html.parser')
    driver.quit()

    # Searching for the list/sale action, collection name, "nft id" and the NFT price in the html code from Opensea
    try:
        action_type = search('h6', 'Blockreact__Block-sc-1xf18x6-0 Textreact__Text-sc-1w94ul3-0 ehCsVi ibqWjk', content).text
        collection_name = search('a', 'styles__StyledLink-sc-l6elh8-0 ekTmzq CollectionLink--link CollectionLink--isSmall', content).text
        nft_id = search('div', 'Overflowreact__OverflowContainer-sc-7qr9y8-0 jRbcys', content).text
        asset_price = search('div', 'Overflowreact__OverflowContainer-sc-7qr9y8-0 jPSCbX Price--amount', content).text
        nft_link = search('a', 'styles__StyledLink-sc-l6elh8-0 ekTmzq styles__CoverLink-sc-nz4knd-1 givILt', content)['href']
        nft_image = search('div', 'Imagereact__DivContainer-sc-dy59cl-0 kMPTZo Image--fade Image--isImageLoaded Image--isImageLoaderVisible AssetMedia--img', content).img['src']
        nft_id = nft_id[:len(nft_id) - 1]
        asset_price = asset_price[:len(asset_price) - 1]

        # Structured in a string all those 4 pieces of data we were able to retrieve in compare_transform variable
        compare_transform = f'{action_type}|{collection_name}|{nft_id}|{asset_price}'
        discord_message = f'**{action_type.upper()}**: {collection_name}, {nft_id}, for the price of: {asset_price} ETH'
    except:
        return "Data corrupted"

    # Comparing if the user made a new action if he did we are re-writing that action as the last one, otherwise nothing
    if compare_transform == previous_action:
        return 'No changes in action'
    else:
        with open("opensea_html.txt", "r+") as file:
            file.seek(0)
            file.truncate(0)
            file.write(f'{action_type}|{collection_name}|{nft_id}|{asset_price}')
        return [discord_message, f'https://opensea.io/{nft_link}', nft_image]
