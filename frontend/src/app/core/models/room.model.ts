import { User } from './user.model';

export interface Room {
  id: string;
  name: string;
  usersCount: number;
  isPasswordProtected: boolean;
  owner: User;
}
