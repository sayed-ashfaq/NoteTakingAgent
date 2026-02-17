
import { useState, useEffect } from "react";
import { useUser, UserButton, useAuth } from "@clerk/clerk-react";
import { Send, Mic, Loader2, FileAudio } from "lucide-react";
import api from "../services/api";

export default function Dashboard() {
    const { user } = useUser();
    const { getToken } = useAuth();
    const [input, setInput] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const [notes, setNotes] = useState<any[]>([]);
    const [audioFile, setAudioFile] = useState<File | null>(null);

    // Fetch notes on load (Mock for now, or actual API if backend running)
    useEffect(() => {
        // fetchNotes(); 
    }, []);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!input && !audioFile) return;

        setIsLoading(true);
        try {
            const formData = new FormData();
            if (input) formData.append("text", input);
            if (audioFile) formData.append("audio", audioFile);

            // Get token properly via Clerk interceptor or manual
            // For this MVP, we rely on the interceptor defined in api.ts? 
            // Wait, api.ts needs `setAuthToken` called. I should do that in App.tsx or useAuth hook.
            // But for now, let's just assume the user sets it up or we pass it here.

            // const res = await api.post("/notes/process", formData);
            // setNotes([res.data, ...notes]);

            // Simulated response for UI testing
            setTimeout(() => {
                setNotes([{
                    id: Date.now(),
                    title: "New Note",
                    category: "Note",
                    formatted_content: input || "Audio Note",
                    status: "Active",
                    target_date: new Date().toISOString().split('T')[0]
                }, ...notes]);
                setInput("");
                setAudioFile(null);
                setIsLoading(false);
            }, 1000);

        } catch (error) {
            console.error("Error submitting note", error);
            setIsLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-slate-950 text-slate-100">
            {/* Header */}
            <header className="border-b border-slate-800 bg-slate-900/50 backdrop-blur-md sticky top-0 z-10">
                <div className="container mx-auto px-6 h-16 flex justify-between items-center">
                    <h1 className="font-bold text-xl">Dashboard</h1>
                    <div className="flex items-center gap-4">
                        <span className="text-sm text-slate-400 hidden sm:inline">Welcome, {user?.firstName}</span>
                        <UserButton afterSignOutUrl="/" />
                    </div>
                </div>
            </header>

            <main className="container mx-auto px-6 py-8 max-w-4xl">
                {/* Input Area */}
                <div className="bg-slate-900 rounded-2xl border border-slate-800 p-6 shadow-xl mb-12">
                    <form onSubmit={handleSubmit} className="space-y-4">
                        <textarea
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            placeholder="What's on your mind? (e.g. 'Remind me to call John tomorrow')"
                            className="w-full bg-slate-950 border border-slate-800 rounded-xl p-4 min-h-[120px] focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none resize-none placeholder-slate-500 transition-all"
                        />

                        <div className="flex justify-between items-center">
                            <div className="flex gap-2">
                                <label className="cursor-pointer p-2 hover:bg-slate-800 rounded-lg transition-colors text-slate-400 hover:text-indigo-400">
                                    <input
                                        type="file"
                                        accept="audio/*"
                                        className="hidden"
                                        onChange={(e) => setAudioFile(e.target.files?.[0] || null)}
                                    />
                                    <Mic className="h-5 w-5" />
                                </label>
                                {audioFile && (
                                    <div className="flex items-center gap-2 text-indigo-400 bg-indigo-900/20 px-3 py-1 rounded-full text-sm">
                                        <FileAudio className="h-4 w-4" />
                                        {audioFile.name}
                                        <button onClick={() => setAudioFile(null)} className="ml-2 hover:text-indigo-200">×</button>
                                    </div>
                                )}
                            </div>

                            <button
                                type="submit"
                                disabled={isLoading || (!input && !audioFile)}
                                className="bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed text-white px-6 py-2.5 rounded-lg font-medium flex items-center gap-2 transition-all"
                            >
                                {isLoading ? <Loader2 className="h-5 w-5 animate-spin" /> : <Send className="h-5 w-5" />}
                                Process
                            </button>
                        </div>
                    </form>
                </div>

                {/* Recent Notes */}
                <div>
                    <h2 className="text-xl font-semibold mb-6 flex items-center gap-2">
                        <span className="w-2 h-8 bg-indigo-500 rounded-full"></span>
                        Recent Activity
                    </h2>

                    <div className="grid gap-4">
                        {notes.length === 0 ? (
                            <div className="text-center py-12 text-slate-500 border border-dashed border-slate-800 rounded-xl">
                                No notes yet. Start typing above!
                            </div>
                        ) : (
                            notes.map((note) => (
                                <div key={note.id} className="bg-slate-900/50 border border-slate-800 p-5 rounded-xl hover:border-indigo-500/30 transition-colors group">
                                    <div className="flex justify-between items-start mb-2">
                                        <span className={`text-xs font-semibold px-2 py-1 rounded-md ${note.category === 'Task' ? 'bg-amber-900/30 text-amber-300' :
                                            note.category === 'Idea' ? 'bg-purple-900/30 text-purple-300' :
                                                'bg-blue-900/30 text-blue-300'
                                            }`}>
                                            {note.category.toUpperCase()}
                                        </span>
                                        <span className="text-xs text-slate-500">{note.target_date}</span>
                                    </div>
                                    <h3 className="font-medium text-lg mb-1 group-hover:text-indigo-300 transition-colors">{note.title}</h3>
                                    <p className="text-slate-400 text-sm line-clamp-2">{note.formatted_content}</p>
                                </div>
                            ))
                        )}
                    </div>
                </div>
            </main>
        </div>
    );
}
