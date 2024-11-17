import { Poem } from "./poem";
import { Review } from "./review";

export interface User {
    id: number;
    firstname: string;
    email: string;
    password?: string;
    admin: boolean;
    poems?: Poem[];
    reviews?: Review[];
  }
  