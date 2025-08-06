import asyncio
from browser_use.llm import ChatGoogle #, ChatOllama
from browser_use import Agent, Controller
from dotenv import load_dotenv
from google import genai
from google.genai import types
from loguru import logger
import os
from pydantic import BaseModel
import random


load_dotenv()

# 📱 Mobile & Tablet Accessories
mobile_keywords = [
    "iPhone 16 pro case", "iPhone 15/16 MagSafe charger", "USB-C fast charger 65W",
    "MagSafe battery pack deal", "Samsung Galaxy S23 case", "iPad stylus pen deal",
    "AirTag key finder", "tablet stand"
]

# 💻 Computers & Office Gear
computer_keywords = [
    "gaming laptop deal", "27-inch 4K monitor sale", "wireless mechanical keyboard",
    "1TB SSD external", "standing desk deal", "ergonomic chair sale"
]

# 🎧 Audio & Streaming
audio_keywords = [
    "noise-canceling headphones sale", "gaming headset for PS5",
    "Bluetooth speaker waterproof deal", "4K streaming webcam"
]

# 🔌 Power & Peripherals
peripheral_keywords = [
    "power bank 20000mAh discount", "surge protector with USB ports",
    "wireless mouse deal", "USB-C hub adapter"
]

# 🏠 Smart Home Gadgets
smart_home_keywords = [
    "smart LED light strips deal", "Wi-Fi smart plug sale", "video doorbell discount",
    "smart thermostat sale"
]

# 🏡 Home & Kitchen Gadgets
home_kitchen_keywords = [
    "robot vacuum on sale", "air fryer discount", "air purifier HEPA deal",
    "countertop icemaker"
]

# 💪 Health & Fitness Tech
fitness_keywords = [
    "massage gun deal", "fitness tracker watch", "wireless scale sale",
    "portable massage chair", "electric toothbrush discount"
]

# 🐾 Pet Tech
pet_keywords = [
    "automatic pet feeder deal", "pet camera treat dispenser",
    "self-cleaning litter box sale", "smart pet water fountain"
]

# 🎁 Seasonal / Gifts
seasonal_keywords = [
    "back to school tech deals", "holiday gift ideas", "Black Friday Amazon deals",
    "Cyber Monday electronics", "Mother’s Day gifts", "Father’s Day gifts",
    "graduation tech gifts"
]

# 🎮 Pop-Culture Tie-ins
pop_keywords = [
    "iPhone 16 case", "PS5 gaming chair", "Nintendo Switch accessories",
    "Star Wars LEGO set deal"
]


high_commission_keywords = [
    "Apple Watch band", "Apple Watch deal", "noise cancelling earbuds",
    "4K TV 55 inch deal", "gaming laptop sale Dell", "ASUS ROG laptop deal",
    "kitchen gadget Amazon coupon", "kitchen hack gadget", "luxury skincare on sale",
    "LED facial mask", "hair styling tool discount", "Mighty Patch acne stickers",
    "heatless curling set", "candle warmer lamp"
]

facebook_hashtags = [
    "#TechDeals", "#AmazonFinds", "#DealAlert", "#DailyDeals",
    "#Gaming", "#Headphones", "#SmartHome", "#PhoneAccessories", "#LaptopDeals",
    "#KitchenGadgets", "#PetTech", "#FitnessDeals", "#BeautyDeals",
    "#BackToSchool", "#HolidaySavings", "#BlackFriday", "#CyberMonday",
    "#MothersDayGifts", "#FathersDayGifts", "#GiftIdeas",
    "#iPhone16", "#USBTypeC", "#4KMonitor", "#PowerBank", "#DogMom", "#CatDad"
]


mobile_accessories
    "iPhone 16 pro case",
    "iPhone 16 pro screen protector",
    "iPhone 16 pro max case",
    "iPhone 15 case deals",
    "MagSafe accessories",
    "Clear iPhone case",
    "iPhone camera protector",
    "iPhone charging cable",
    "Wireless mouse",
    "Wireless charging pad",
    "Battery bank",
    "Phone grip holder",
    "Car phone mount",
    "iPhone lens attachment",
]


tech_accessories = [
    "USB-C accessories",
    "Fast charging block",
    "Portable charger 20000mah",
    "Laptop stand adjustable",
    "Mechanical keyboard budget",
    "RGB gaming mouse",
    "Webcam with ring light",
    "Bluetooth earbuds under $50",
    "Cable organizer desk",
    "Monitor light bar",
]


back_to_school = [
    "Student laptop bag",
    "Study desk organizer",
    "Noise cancelling headphones studying",
    "iPad accessories students",
    "Backpack with USB port",
]


gift_holiday = [
    "Tech gifts under $25",
    "Stocking stuffers tech",
    "Gift ideas iPhone users",
    "Bluetooth tracker keys",
    "Smart home starter kit",
]


home_office = [
    "Standing desk converter",
    "Ergonomic mouse pad",
    "Blue light glasses",
    "Desk cable management",
    "Monitor arm mount",
]


smart_home = [
    "Smart plug Alexa",
    "LED strip lights",
    "Security camera indoor",
    "Smart light bulbs",
    "Video doorbell",
]


fitness_tech = [
    "Fitness tracker under $30",
    "Bluetooth scale",
    "Foam roller electric",
    "Resistance bands set",
    "Yoga mat thick"
]


hashtags = [
    "#iPhoneDeals",
    "#TechFinds",
    "#AmazonFinds",
    "#PhoneAccessories",
    "#TechLovers",
    "#GadgetAddict",
    "#DailyDeals",
    "#FlashSale",
    "#LimitedTimeOffer",
    "#TechUnder20",
    "#BudgetTech",
    "#TechReview",
    "#MustHave2025",
    "#TechEssentials",
    "#WorkFromHome"
]


class AmazonItem(BaseModel):
    name: str
    description: str
    url: str
    price: str
    discount_amount: str
    rating: str
    amount_of_reviews: str
    review_summary: str | None = ""


def create_conversation_folder(folder_name: str):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name, exist_ok=True)


async def get_item_info(prompt: str, conversation_folder: str) -> str:
    # Initialize the model
    llm = ChatGoogle(model='gemini-2.5-flash-lite')

    # Header for the agent
    header = { 
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9,he;q=0.8",
        "upgrade-insecure-requests": 1,
    }

    # Controller
    controller = Controller(output_model=AmazonItem)
    # Create agent with the model
    agent = Agent(
        task=prompt,
        llm=llm,
        save_conversation_path=f"./{conversation_folder}/",
        header=header,
        controller=controller
    )
    result = await agent.run()
    
    # Print the final result (call the method)
    logger.debug("Final Result:")
    logger.debug(result.final_result())
    return result.final_result()


def generate_facebook_post(item_info: str) -> str:
    client = genai.Client()
    model = "gemini-2.5-flash"
    prompt = f"""
You are a Facebook page post generator expert. You are familiar with Amazon Affiliate rules and best practices, and Facebook page post best practices.
Generate a Facebook page post that will be viral, and engaging, following Amazon Affiliate rules, should be short, precise and engaging
Add all the following hash tags in one line at the end of the post
#Amazon #onlineshop #onlineshopping #sale #ad #affiliatemarketing #discounts #amazonfinds

If there are more appropriate hashtags to add that can increase reach, add them.

This is the context to create the ad from:

{item_info}

"""
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="text/plain",
            temperature=0.2
        )
    )
    return response.text



async def main():
    conversation_folder = "conversations"
    create_conversation_folder(conversation_folder)
    search_terms = [
        "iPhone 16 pro case",
        "iPhone 16 pro screen protector",
        "Wireless mouse",
        "Battery bank",
    ]
    random_search_term = random.choice(search_terms)
    prompt = f"""
        Go to Amazon.com and search for {random_search_term} on sales with a discount of at least 20%.
        Reruen the item correct item URL, item name, description, discount amount, rating, amount of reviews, review summary, and the price. 
        If you can't find appropriate one, at the end of the page you can go to the next page, it will be a number between previous and next page div",
        """
    result = await get_item_info(prompt, conversation_folder)
    if result is None:
        logger.error("No item found")
        return
    
    facebook_post = generate_facebook_post(result)
    print(facebook_post)


if __name__ == "__main__":
    asyncio.run(main())
