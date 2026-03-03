import { Link, useLocation } from "react-router-dom";
import { Activity } from "lucide-react";

const Header = () => {
  const location = useLocation();

  return (
    <header className="sticky top-0 z-50 border-b border-border bg-card/80 backdrop-blur-md">
      <div className="container mx-auto flex h-16 items-center justify-between px-4">
        <Link to="/" className="flex items-center gap-2.5">
          <div className="flex h-9 w-9 items-center justify-center rounded-lg gradient-hero">
            <Activity className="h-5 w-5 text-primary-foreground" />
          </div>
          <span className="text-lg font-semibold tracking-tight text-foreground">
            PostureAI
          </span>
        </Link>
        <nav className="flex items-center gap-1">
          <Link
            to="/"
            className={`rounded-md px-4 py-2 text-sm font-medium transition-colors ${
              location.pathname === "/"
                ? "bg-secondary text-foreground"
                : "text-muted-foreground hover:text-foreground"
            }`}
          >
            Home
          </Link>
          <Link
            to="/analysis"
            className={`rounded-md px-4 py-2 text-sm font-medium transition-colors ${
              location.pathname === "/analysis"
                ? "bg-secondary text-foreground"
                : "text-muted-foreground hover:text-foreground"
            }`}
          >
            Analysis
          </Link>
        </nav>
      </div>
    </header>
  );
};

export default Header;
