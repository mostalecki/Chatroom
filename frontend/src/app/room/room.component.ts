import { Component, OnInit } from '@angular/core';
import { FormControl } from '@angular/forms';
import { ActivatedRoute, Router } from '@angular/router';

import { Room, RoomService, Comment, User, UserService } from '../core';
import { MatDialog, MatDialogConfig } from '@angular/material/dialog';
import { RoomDialogComponent } from './room-dialog.component';
import { WebsocketTicketService } from 'app/core/services/websocket-ticket.service';
import { Ticket } from 'app/core/models/websocket-ticket.model';

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
  canConnect = false;
  username: string;
  password: string;
  token: string;

  constructor(
    private route: ActivatedRoute,
    private roomService: RoomService,
    //private commentsService: CommentsService,
    private router: Router,
    private userService: UserService,
    private ticketService: WebsocketTicketService,
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

    if (!this.currentUser.username || this.room.isPasswordProtected) {
      this.openDialog();
    } else {
      this.connect();
    }
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

    dialogRef.afterClosed().subscribe((data) => {
      this.username = data.username;
      this.password = data.password;
      this.connect();
    });
  }

  connect() {
    if (this.currentUser.username) {
      this.ticketService.get().subscribe((ticket: Ticket) => {
        //throw new Error(data);
        this.token = ticket.token;
        this.canConnect = true;
      });
    } else {
      this.canConnect = true;
    }
  }
}
