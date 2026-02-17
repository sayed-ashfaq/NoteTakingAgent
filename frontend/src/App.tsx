
import { SignedIn, SignedOut, SignIn, SignUp, useUser } from "@clerk/clerk-react";
import { BrowserRouter, Route, Routes, useNavigate, Navigate } from "react-router-dom";
import Landing from "./pages/Landing";
import Dashboard from "./pages/Dashboard";

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Landing />} />

                {/* Auth Routes */}
                <Route path="/sign-in/*" element={
                    <div className="flex items-center justify-center min-h-screen">
                        <SignIn routing="path" path="/sign-in" />
                    </div>
                } />
                <Route path="/sign-up/*" element={
                    <div className="flex items-center justify-center min-h-screen">
                        <SignUp routing="path" path="/sign-up" />
                    </div>
                } />

                {/* Protected Dashboard */}
                <Route
                    path="/dashboard"
                    element={
                        <>
                            <SignedIn>
                                <Dashboard />
                            </SignedIn>
                            <SignedOut>
                                <Navigate to="/sign-in" />
                            </SignedOut>
                        </>
                    }
                />
            </Routes>
        </BrowserRouter>
    );
}

export default App;
