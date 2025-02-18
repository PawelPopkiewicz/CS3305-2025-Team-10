import {Trip} from "@/types/trip";

export type Stop = {
    id: number;
    name: string;
    latitude: number;
    longitude: number;
    tripIds: Trip[];
}