import { ModuleWithProviders, NgModule } from '@angular/core';
import { MatDialogModule, MatDialog } from '@angular/material/dialog';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';

import { RoomListComponent } from './room-list.component';
import { RoomPreviewComponent } from './room-preview.component';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { RouterModule } from '@angular/router';
import { RoomMetaComponent } from './room-meta.component';
import { RoomCreateButtonComponent } from './room-create-button.component';
import { RoomRoutingModule } from './room-routing.module';
import { RoomComponent } from './room.component';
import { RoomResolver } from './room-resolver.service';
import { RoomService } from 'app/core';
import { RoomDialogComponent } from './room-dialog.component';
import { WebsocketTicketService } from 'app/core/services/websocket-ticket.service';
import { ChatModule } from 'app/chat/chat.module';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
    RouterModule,
    RoomRoutingModule,
    MatDialogModule,
    MatInputModule,
    MatSelectModule,
    ChatModule,
  ],
  declarations: [
    RoomComponent,
    RoomListComponent,
    RoomPreviewComponent,
    RoomMetaComponent,
    RoomDialogComponent,
    RoomCreateButtonComponent,
  ],
  exports: [
    RoomListComponent,
    RoomPreviewComponent,
    RoomMetaComponent,
    RoomCreateButtonComponent,
  ],
  providers: [RoomResolver, RoomService, WebsocketTicketService],
  entryComponents: [RoomDialogComponent],
})
export class RoomModule {}
