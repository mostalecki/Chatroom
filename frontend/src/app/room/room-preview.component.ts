import { Component, Input } from '@angular/core';
import { Room } from 'app/core';

@Component({
  selector: 'app-room-preview',
  templateUrl: './room-preview.component.html',
})
export class RoomPreviewComponent {
  @Input() room: Room;
}
