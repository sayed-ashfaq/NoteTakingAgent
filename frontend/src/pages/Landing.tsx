
import { Link } from "react-router-dom";
import { ArrowRight, Mic, Sparkles, Zap } from "lucide-react";
import { useAuth } from "@clerk/clerk-react";
import { useEffect } from "react";
import { useNavigate } from "react-router-dom";

export default function Landing() {
    const { isSignedIn } = useAuth();
    const navigate = useNavigate();

    useEffect(() => {
        if (isSignedIn) navigate("/dashboard");
    }, [isSignedIn, navigate]);

    return (
        <div className="min-h-screen bg-slate-950 text-white selection:bg-indigo-500/30">
            {/* Navigation */}
            <nav className="container mx-auto px-6 py-6 flex justify-between items-center">
                <div className="flex items-center space-x-2">
                    <Sparkles className="h-6 w-6 text-indigo-500" />
                    <span className="font-bold text-xl tracking-tight">SmartNotes</span>
                </div>
                <div className="space-x-4">
                    <Link to="/sign-in" className="text-slate-300 hover:text-white transition-colors">Sign In</Link>
                    <Link to="/sign-up" className="bg-indigo-600 hover:bg-indigo-700 px-4 py-2 rounded-lg font-medium transition-all">
                        Get Started
                    </Link>
                </div>
            </nav>

            {/* Hero Section */}
            <main className="container mx-auto px-6 pt-20 pb-32 text-center">
                <div className="inline-flex items-center px-4 py-2 rounded-full bg-indigo-900/30 border border-indigo-500/20 text-indigo-300 mb-8 animate-fade-in-up">
                    <span className="text-sm font-medium">✨ Powered by Advanced AI</span>
                </div>

                <h1 className="text-5xl md:text-7xl font-bold mb-8 bg-gradient-to-r from-white via-slate-200 to-slate-400 text-transparent bg-clip-text leading-tight">
                    Capture thoughts.<br />
                    <span className="text-indigo-400">Organize effortlessly.</span>
                </h1>

                <p className="text-xl text-slate-400 mb-12 max-w-2xl mx-auto leading-relaxed">
                    Transform your voice and text notes into actionable tasks and structured pages in Notion automatically.
                </p>

                <div className="flex flex-col sm:flex-row justify-center gap-4">
                    <Link to="/sign-up" className="group flex items-center justify-center gap-2 bg-indigo-600 hover:bg-indigo-700 px-8 py-4 rounded-xl text-lg font-semibold transition-all hover:scale-105 shadow-lg shadow-indigo-500/25">
                        Try for free
                        <ArrowRight className="h-5 w-5 group-hover:translate-x-1 transition-transform" />
                    </Link>
                    <a href="#features" className="flex items-center justify-center gap-2 bg-slate-800 hover:bg-slate-700 px-8 py-4 rounded-xl text-lg font-medium transition-all">
                        Learn more
                    </a>
                </div>

                {/* Feature Grid */}
                <div id="features" className="mt-32 grid md:grid-cols-3 gap-8 text-left">
                    <FeatureCard
                        icon={<Mic className="h-6 w-6 text-blue-400" />}
                        title="Voice to Text"
                        desc="Speak your mind. We transcribe and format it instantly using Whisper AI."
                    />
                    <FeatureCard
                        icon={<Zap className="h-6 w-6 text-amber-400" />}
                        title="Instant Action"
                        desc="AI detects tasks and adds them to your todo list automatically."
                    />
                    <FeatureCard
                        icon={<Sparkles className="h-6 w-6 text-purple-400" />}
                        title="Notion Sync"
                        desc="Seamlessly pushes formatted notes and tasks to your Notion workspace."
                    />
                </div>
            </main>
        </div>
    );
}

function FeatureCard({ icon, title, desc }: { icon: any, title: string, desc: string }) {
    return (
        <div className="p-8 rounded-2xl bg-slate-900/50 border border-slate-800 hover:border-slate-700 transition-colors">
            <div className="mb-4 p-3 bg-slate-800/50 rounded-lg inline-block w-fit">
                {icon}
            </div>
            <h3 className="text-xl font-semibold mb-2">{title}</h3>
            <p className="text-slate-400 leading-relaxed">{desc}</p>
        </div>
    )
}
