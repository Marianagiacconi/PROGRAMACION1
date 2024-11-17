import { User } from './user';
import { Poem } from './poem';

export interface Review {
  id: number;
  userID: number;
  poemID: number;
  score: number;
  comment: string;
  user?: User;
  poems?: Poem;
}
