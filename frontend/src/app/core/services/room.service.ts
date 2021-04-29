import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { ApiService } from './api.service';
import { Room, RoomListConfig } from '../models';
import { map } from 'rxjs/operators';
import { HttpParams } from '@angular/common/http';

@Injectable()
export class RoomService {
  constructor(private apiService: ApiService) {}

  list(config: RoomListConfig): Observable<{ results: Room[]; count: number }> {
    // Convert any filters over to Angular's URLSearchParams
    const params = {};

    Object.keys(config.filters).forEach((key) => {
      params[key] = config.filters[key];
    });

    return this.apiService.get(
      '/rooms',
      new HttpParams({ fromObject: params })
    );
  }

  get(id: string): Observable<Room> {
    return this.apiService.get('/rooms/' + id).pipe(map((room: Room) => room));
  }

  create(data): Observable<Room> {
    return this.apiService
      .post('/rooms/', { ...data })
      .pipe(map((room: Room) => room));
  }
}
