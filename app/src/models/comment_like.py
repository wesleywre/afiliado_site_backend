from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship
from src.core.database import Base


class CommentLike(Base):
    __tablename__ = "comment_likes"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    comment_id = Column(Integer, ForeignKey("comments.id"), nullable=False)

    __table_args__ = (UniqueConstraint("user_id", "comment_id", name="_user_comment_uc"),)

    user = relationship("User", back_populates="comment_likes")
    comment = relationship("Comment", back_populates="likes")
