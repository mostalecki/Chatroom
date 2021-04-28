import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-room-create-button',
  templateUrl: './room-create-button.component.html',
})
export class RoomCreateButtonComponent {
  constructor(private router: Router) {}

  roomCreateDialog() {}
}
