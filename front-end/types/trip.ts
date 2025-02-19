import {Bus} from "@/types/bus";
import {Stop} from "@/types/stop";

export type Trip = {
    id: string;
    bus: Bus;
    stop: Stop;
    incoming_time: number;
}