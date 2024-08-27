from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth
from ..database import get_db


router = APIRouter(prefix='/vote', tags=["Votes"])


### user_id will be accessed through token. Req obj should have post id and vote_dir(0=liked, 1=unliked)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.VoteCast, current_user: int = Depends(oauth.get_current_user), db: Session = Depends(get_db)):

    # query to see if vote already exists given the current post and curr user
    vote_query = db.query(models.Vote).filter(models.Vote.user_id == current_user.id, models.Vote.post_id == vote.post_id)
    found_vote = vote_query.first()
    
    if(vote.vote_dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {current_user.id} has alredy liked post {vote.post_id}.")
        
        # add logic to like voteif found vote is null
        new_vote = models.Vote(post_id=vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message":"Successfully added vote"}

    else:
        # cant delete vote that does not exist
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        
        # add logic to unlike vote
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"Vote deleted"}