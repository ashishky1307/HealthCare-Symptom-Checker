import { SignIn } from "@clerk/nextjs";

export default function SignInPage() {
    return (
        // Container: Full screen height, centered content, professional gradient background
        <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-slate-900 via-blue-900 to-indigo-900 p-4">
            {/* The Clerk SignIn Component */}
            <SignIn
                appearance={{
                    elements: {
                        // Professional styling with enhanced shadow and border
                        card: "shadow-2xl border-2 border-indigo-200 bg-white",
                        headerTitle: "text-slate-800 font-bold",
                        headerSubtitle: "text-slate-600",
                    },
                }}
            />
        </div>
    );
}