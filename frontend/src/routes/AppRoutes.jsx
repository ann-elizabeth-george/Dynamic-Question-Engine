import { Routes, Route } from "react-router-dom";

import Welcome from "../pages/Welcome";

import NamePage from "../pages/registration/NamePage";
import MobilePage from "../pages/registration/MobilePage";
import DistrictPage from "../pages/registration/DistrictPage";
import AgePage from "../pages/registration/AgePage";
export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Welcome />} />

      <Route path="/register/name" element={<NamePage />} />

      <Route path="/register/mobile" element={<MobilePage />} />
<Route
  path="/register/age"
  element={<AgePage />}
/>
<Route path="/register/district" element={<DistrictPage />} />
    </Routes>
  );
}