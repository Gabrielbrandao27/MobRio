import axiosInstance from "./axiosConfig.ts";

export const landingPage = async () => {
  try {
    const response = await axiosInstance.get(`/`);
    return response.data;
  } catch (error) {
    console.error("Error on landing page:", error);
    throw error;
  }
};

export const homePage = async () => {
  try {
    const response = await axiosInstance.get(`/home`);
    return response.data;
  } catch (error) {
    console.error("Error on home page:", error);
    throw error;
  }
};

export const registerPage = async (
  name: string,
  password: string,
  email: string
) => {
  try {
    const payload = {
      name,
      password,
      email,
    };
    const response = await axiosInstance.post(`/register`, payload);
    return response.data;
  } catch (error) {
    console.error("Error on register page:", error);
    throw error;
  }
};

export const loginPage = async (email: string, password: string) => {
  try {
    const payload = {
      email,
      password,
    };
    const response = await axiosInstance.post(`/login`, payload);
    return response.data;
  } catch (error) {
    console.error("Error on landing page:", error);
    throw error;
  }
};

export const busRoutes = async () => {
  try {
    const response = await axiosInstance.get(`/bus/routes`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching bus routes:", error);
    throw error;
  }
};

export const busStops = async (routeId: string, directionId: number) => {
  try {
    const response = await axiosInstance.get(
      `/bus/stops?route_id=${routeId}&direction_id=${directionId}`,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      }
    );
    return response.data;
  } catch (error) {
    console.error("Error fetching bus stops:", error);
    throw error;
  }
};

export const userBusRelation = async (
  routeStopId: string,
  openTime: string,
  closeTime: string
) => {
  try {
    const payload = {
      route_stop_id: routeStopId,
      open_time: openTime,
      close_time: closeTime,
    };
    const response = await axiosInstance.post(`/user_bus_relation`, payload, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    });
    return response.data;
  } catch (error) {
    console.error("Error posting user bus relation:", error);
    throw error;
  }
};

export const busLivePositions = async () => {
  try {
    const response = await axiosInstance.get(`/bus/live_positions`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching bus live positions:", error);
    throw error;
  }
};
