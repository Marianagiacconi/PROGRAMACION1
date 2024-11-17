import { User } from './user';
import { Review } from './review';

export interface Poem {
  id: number;
  title: string;
  content: string;
  userID: number;
  user?: User;
  reviews?: Review[];
}
