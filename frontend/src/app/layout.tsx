import "./globals.css";

export const metadata = {
  title: "Bioluminescent Detection AI",
  description:
    "AI-powered bioluminescent bead detection distance prediction system",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50">
        {children}
      </body>
    </html>
  );
}
