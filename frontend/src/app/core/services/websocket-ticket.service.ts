import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { ApiService } from './api.service';
import { map } from 'rxjs/operators';
import { Ticket } from '../models/websocket-ticket.model';

@Injectable()
export class WebsocketTicketService {
  constructor(private apiService: ApiService) {}

  get(): Observable<Ticket> {
    return this.apiService
      .post('/tickets/')
      .pipe(map((ticket: Ticket) => ticket));
  }
}
