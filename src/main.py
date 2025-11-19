from fastapi import FastAPI

from supertokens_python import init, InputAppInfo, SupertokensConfig
from supertokens_python.recipe import session, emailpassword
from supertokens_python.framework.fastapi import get_middleware

from src.api import main_router

# Ну возьмите пжка

init(
    app_info=InputAppInfo(
        app_name="AudioNotes",
        api_domain="http://localhost:8000",
        website_domain="http://localhost:3000",
        api_base_path="/auth",
        website_base_path="/auth"
    ),
    supertokens_config=SupertokensConfig(
        connection_uri="https://try.supertokens.com"
    ),
    recipe_list=[
        session.init(),
        emailpassword.init(),
    ],
    framework='fastapi'
)

app = FastAPI()

#app.add_middleware(get_middleware())

app.include_router(main_router)
