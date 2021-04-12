import { ModuleWithProviders, NgModule } from '@angular/core';

import { RoomListComponent } from './room-list.component';
import { RoomPreviewComponent } from './room-preview.component';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { RouterModule } from '@angular/router';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
    RouterModule,
  ],
  declarations: [RoomListComponent, RoomPreviewComponent],
  exports: [RoomListComponent, RoomPreviewComponent],
})
export class RoomModule {}
