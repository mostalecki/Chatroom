import { Component, OnInit } from '@angular/core';
import { FormControl } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';

import { Room, RoomService, Comment, User, UserService } from '../core';
import { MatDialog, MatDialogConfig } from '@angular/material/dialog';
import { RoomDialogComponent } from './room-dialog.component';

@Component({
  selector: 'app-room-page',
  templateUrl: './room.component.html',
  providers: [RoomService],
})
export class RoomComponent implements OnInit {
  room: Room;
  currentUser: User;
  canModify: boolean;
  comments: Comment[];
  commentControl = new FormControl();
  commentFormErrors = {};
  isSubmitting = false;
  isDeleting = false;

  constructor(
    private route: ActivatedRoute,
    private roomService: RoomService,
    //private commentsService: CommentsService,
    private router: Router,
    private userService: UserService,
    private dialog: MatDialog
  ) {}

  ngOnInit() {
    // Retreive the prefetched article
    this.route.data.subscribe((data: { room: Room }) => {
      this.room = data.room;

      // Load the comments on this article
      //this.populateComments();
    });

    // Load the current user's data
    this.userService.currentUser.subscribe((userData: User) => {
      this.currentUser = userData;

      this.canModify = this.currentUser.username === this.room.owner.username;
    });

    this.openDialog();
  }

  openDialog() {
    const dialogConfig = new MatDialogConfig();

    dialogConfig.disableClose = true;
    dialogConfig.autoFocus = true;
    dialogConfig.data = {
      username: this.currentUser.username,
      isPasswordProtected: this.room.isPasswordProtected,
    };

    const dialogRef = this.dialog.open(RoomDialogComponent, dialogConfig);

    dialogRef.afterClosed().subscribe((data) => console.log(data));
  }

  /*onToggleFavorite(favorited: boolean) {
    this.article.favorited = favorited;

    if (favorited) {
      this.article.favoritesCount++;
    } else {
      this.article.favoritesCount--;
    }
  }*/

  /*onToggleFollowing(following: boolean) {
    this.article.author.following = following;
  }

  deleteArticle() {
    this.isDeleting = true;

    this.articlesService.destroy(this.article.slug).subscribe((success) => {
      this.router.navigateByUrl('/');
    });
  }

  populateComments() {
    this.commentsService
      .getAll(this.article.slug)
      .subscribe((comments) => (this.comments = comments));
  }

  addComment() {
    this.isSubmitting = true;
    this.commentFormErrors = {};

    const commentBody = this.commentControl.value;
    this.commentsService.add(this.article.slug, commentBody).subscribe(
      (comment) => {
        this.comments.unshift(comment);
        this.commentControl.reset('');
        this.isSubmitting = false;
      },
      (errors) => {
        this.isSubmitting = false;
        this.commentFormErrors = errors;
      }
    );
  }

  onDeleteComment(comment) {
    this.commentsService
      .destroy(comment.id, this.article.slug)
      .subscribe((success) => {
        this.comments = this.comments.filter((item) => item !== comment);
      });
  }*/
}
