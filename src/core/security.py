from fastapi import Depends, HTTPException
from supertokens_python.recipe.session.framework.fastapi import verify_session
from supertokens_python.recipe.session.asyncio import get_session


async def get_current_user_id(session=Depends(verify_session())):
    return session.get_user_id()