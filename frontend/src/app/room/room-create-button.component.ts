import { Component, EventEmitter, Input, Output } from '@angular/core';
import { MatDialog, MatDialogConfig } from '@angular/material/dialog';
import { Router } from '@angular/router';
import { RoomCreateDialogComponent } from './room-create-dialog.component';
import { RoomService } from 'app/core';

@Component({
  selector: 'app-room-create-button',
  templateUrl: './room-create-button.component.html',
})
export class RoomCreateButtonComponent {
  constructor(
    private roomService: RoomService,
    private router: Router,
    private dialog: MatDialog
  ) {}

  roomCreateDialog() {
    const dialogConfig = new MatDialogConfig();

    dialogConfig.disableClose = true;
    dialogConfig.autoFocus = true;

    const dialogRef = this.dialog.open(RoomCreateDialogComponent, dialogConfig);

    dialogRef.afterClosed().subscribe((data) => {
      this.createRoom(data);
    });
  }

  createRoom(data: any) {
    console.log(data);
  }
}
