import {Trip} from "@/types/trip";

export type Bus = {
    id: number;
    route: string;
    latitude: number;
    longitude: number;
    direction: number;
    headsign: string;
    stops: Trip[];
};
