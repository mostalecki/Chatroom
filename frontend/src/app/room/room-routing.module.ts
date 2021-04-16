import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { RoomResolver } from './room-resolver.service';
import { RoomComponent } from './room.component';

const routes: Routes = [
  {
    path: 'room/:slug',
    component: RoomComponent,
    resolve: {
      room: RoomResolver,
    },
  },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class RoomRoutingModule {}
