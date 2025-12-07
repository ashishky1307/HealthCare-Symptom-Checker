import { SignUp } from "@clerk/nextjs";

export default function SignUpPage() {
  return (
    // Container: Full screen height, centered content, gradient background
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      {/* The Clerk SignUp Component */}
      <SignUp
        appearance={{
          elements: {
            card: "shadow-xl border border-gray-100",
          },
        }}
      />
    </div>
  );
}