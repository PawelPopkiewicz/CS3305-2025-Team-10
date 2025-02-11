import { configureStore } from "@reduxjs/toolkit";
import busReducer from "./busSlice";

export const store = configureStore({
    reducer: {
        bus: busReducer,
    },
});
export type RootState = ReturnType<typeof store.getState>;