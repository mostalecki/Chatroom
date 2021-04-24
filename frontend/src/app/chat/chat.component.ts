import { Component, NgZone, OnDestroy, OnInit, Input } from '@angular/core';
import { environment } from 'environments/environment';

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css'],
})
export class ChatComponent implements OnInit, OnDestroy {
  title = 'client';
  message = '';
  messages: any[];
  socket: WebSocket;

  constructor(private zone: NgZone) {}
  @Input() roomId: string;
  @Input() username: string;
  @Input() token: string;
  @Input() password: string;

  ngOnInit(): void {
    this.messages = [];
    this.socket = new WebSocket(
      `${environment.api_url}/chat/${this.roomId}?${
        this.token ? 'token=' + this.token : 'username=' + this.username
      }${this.password ? '&password=' + this.password : ''}`
    );
    this.socket.onmessage = (event) => {
      console.log('onmessage:' + event);
      this.zone.run(() => {
        this.addMessage(event.data);
      });
    };
  }

  addMessage(msg: any) {
    this.messages = [...this.messages, msg];
    //console.log("messages::" + this.messages);
  }

  ngOnDestroy(): void {
    this.socket && this.socket.close();
  }

  sendMessage() {
    console.log('sending message:' + this.message);
    this.socket.send(this.message);
    this.message = null;
  }
}
