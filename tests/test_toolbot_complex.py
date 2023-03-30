# flake8: noqa
from ward import test

from turbo_chat import *
from turbo_chat import tool_bot

products = {
    21: "Classic Tweed suit",
    22: "Royal Blue suit",
    23: "Ketterdam leather shoes",
}  # id -> name

cart = {}  # id -> count


def render_cart():
    global cart

    if not cart:
        return "Cart:\nempty"

    items = "\n- ".join(
        [f"id {id} | {products[id]} | {qty}" for id, qty in cart.items()]
    )

    return f"Cart:\nProduct ID | Product Name | Quantity\n- {items}"


async def SearchProducts(query: str) -> str:
    """use this tool to search for products based on the user’s needs. The search query must be in plain English."""

    return (
        "The Classic Tweed suit (product id: 21) and the Royal Blue suit (product id: 22) are great options for men's wedding attire"
        if "shoes" not in query
        else "The Ketterdam leather shoes (product id: 23) are a great pair of shoes"
    )


async def AddProductToCart(product_id: int, quantity: int) -> str:
    """when the user wants to add a product to their cart, first make sure to ask them what quantity they need and then use this tool to add that product to the cart. The tool needs the product id and the quantity to add."""

    global cart

    cart[product_id] = cart.get(product_id, 0) + quantity
    return f"Added {quantity} {products[product_id]} to cart"


async def RecommendSimilarProducts(product_id: int) -> str:
    """use this tool to get recommendations for other products similar to a product of your choosing. It needs the product id of the product you chose to ask recommendations for."""

    return "Recommended: The Ketterdam leather shoes (product id: 23) are a great addition to our wedding suits."


tools = [
    SearchProducts,
    AddProductToCart,
    RecommendSimilarProducts,
]


@turbo()
async def app(
    assistant_gender="female",
    assistant_designation="sales rep",
    store_name="Julep Fashion Company",
    assistant_name="Julia",
    assistant_persona="friendly, helpful and polite",
    product_categories="apparel and fashion accessories",
    product_names=["shoes", "coats", "suits"],
    additional_store_info="",
):
    three_p, more = product_names[:3], product_names[3:]
    up_to_three_product_names = ", ".join(three_p)

    prologue = f"""
You are a {assistant_gender} AI {assistant_designation} for {store_name}. Your name is {assistant_name}. You are {assistant_persona}.

{store_name} sells {product_categories} like {up_to_three_product_names} {"and other products" if more else ""}. {additional_store_info}
""".strip()

    yield System(
        content=prologue
        + "\n"
        + "You are chatting with the customer, start by greeting the customer politely.",
    )

    output = yield Generate(temperature=0.9, forward=False)
    message = output.content

    while True:
        input = yield GetInput(content=message)

        bot = tool_bot(
            prologue=prologue,
            user_type="Customer",
            instruction="Assist the customer with any questions they have about the store or products and help them place orders when they are ready.",
            initial_state=render_cart(),
            tools=tools,
        )

        await bot.run()

        output = await bot.run(dict(input=input, state=render_cart()))
        message = output.content["response"]


@test("contains returns True when toolbot works")
async def test_toolbot_complex():
    bot = app()
    await bot.run()

    output = await bot.run(
        {
            "input": "I am looking for sommething to wear for my friend's wedding",
            "state": render_cart(),
        }
    )

    assert products[21].lower() in output.content.lower()
