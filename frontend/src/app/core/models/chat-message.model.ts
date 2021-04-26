import { ChatUser } from './chat-user.model';

export interface ChatMessage {
  type: string;
  message: string;
  user: ChatUser;
}
