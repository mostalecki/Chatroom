import { Component, NgZone, OnDestroy, OnInit, Input } from '@angular/core';
import { environment } from 'environments/environment';
import { ChatUser } from 'app/core/models/chat-user.model';
import { ChatMessage } from 'app/core/models/chat-message.model';

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css'],
})
export class ChatComponent implements OnInit, OnDestroy {
  title = 'client';
  message = '';
  messages: ChatMessage[];
  users: ChatUser[];
  socket: WebSocket;

  constructor(private zone: NgZone) {}
  @Input() roomId: string;
  @Input() username: string;
  @Input() token: string;
  @Input() password: string;

  ngOnInit(): void {
    this.messages = [];
    this.socket = new WebSocket(
      `${environment.websocket_url}/chat/${this.roomId}?${
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
    let messageObj: ChatMessage = JSON.parse(msg);
    switch (messageObj.type) {
      case 'user_list':
        this.users = messageObj.users;
        break;

      case 'join_message':
        this.users = [...this.users, messageObj.user];
        this.messages = [
          ...this.messages,
          {
            type: 'join_message',
            message: `${messageObj.user.username} has joined.`,
            user: null,
            users: null,
          },
        ];
        break;

      case 'leave_message':
        let user = messageObj.user;
        let userIndex = user.is_user_authenticated
          ? this.users.findIndex((u) => u.username === user.username)
          : this.users.findIndex((u) => u.connection_id === user.connection_id);
        this.messages = [
          ...this.messages,
          {
            type: 'leave_message',
            message: `${user.username} has left.`,
            user: null,
            users: null,
          },
        ];
        delete this.users[userIndex];
        break;

      default:
        this.messages = [...this.messages, messageObj];
        break;
    }
  }

  ngOnDestroy(): void {
    this.socket && this.socket.close();
  }

  sendMessage() {
    this.socket.send(JSON.stringify({ message: this.message }));
    this.message = null;
  }
}
