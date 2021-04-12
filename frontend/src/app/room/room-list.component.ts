import { Component, Input } from '@angular/core';
import { RoomService, RoomListConfig, Room } from 'app/core';

@Component({
  selector: 'app-room-list',
  styleUrls: ['room-list.component.css'],
  templateUrl: './room-list.component.html',
  providers: [RoomService],
})
export class RoomListComponent {
  constructor(private roomService: RoomService) {}

  @Input() limit: number;
  @Input()
  set config(config: RoomListConfig) {
    if (config) {
      this.query = config;
      this.currentPage = 1;
      this.runQuery();
    }
  }

  query: RoomListConfig;
  results: Room[];
  loading = false;
  currentPage = 1;
  totalPages: Array<number> = [1];

  setPageTo(pageNumber) {
    this.currentPage = pageNumber;
    this.runQuery();
  }

  runQuery() {
    this.loading = true;
    this.results = [];

    // Create limit and offset filter (if necessary)
    if (this.limit) {
      this.query.filters.limit = this.limit;
      this.query.filters.offset = this.limit * (this.currentPage - 1);
    }

    this.roomService.list(this.query).subscribe((data) => {
      //throw new Error(data);
      this.loading = false;
      this.results = data;

      var roomsCount = 10;

      // Used from http://www.jstips.co/en/create-range-0...n-easily-using-one-line/
      this.totalPages = Array.from(
        new Array(Math.ceil(roomsCount / this.limit)),
        (val, index) => index + 1
      );
    });
  }
}
