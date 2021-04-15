import { Component, Input } from '@angular/core';
import { Room } from 'app/core';

@Component({
  selector: 'app-room-meta',
  templateUrl: './room-meta.component.html',
})
export class RoomMetaComponent {
  @Input() room: Room;
}
