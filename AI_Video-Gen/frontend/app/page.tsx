"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Card } from "@/components/ui/card";
import { VideoIcon, Download, Loader2 } from "lucide-react";
import { useToast } from "@/hooks/use-toast";

export default function Home() {
  const [topic, setTopic] = useState("");
  const [background, setBackground] = useState("");
  const [loading, setLoading] = useState(false);
  const [videoUrl, setVideoUrl] = useState<string | null>(null);
  const { toast } = useToast();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/generate-video`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ topic, background }),
      });

      if (!response.ok) {
        throw new Error("Failed to generate video");
      }

      const data = await response.json();
      setVideoUrl(data.videoUrl);
      toast({
        title: "Success!",
        description: "Your video has been generated successfully.",
      });
    } catch (error) {
      toast({
        variant: "destructive",
        title: "Error",
        description: "Failed to generate video. Please try again.",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gradient-to-b from-background to-muted">
      <div className="container max-w-4xl mx-auto px-4 py-16">
        <div className="space-y-8">
          <div className="text-center space-y-4">
            <h1 className="text-4xl font-bold tracking-tight">AI Video Generator</h1>
            <p className="text-muted-foreground text-lg">
              Transform your ideas into engaging videos with the power of AI
            </p>
          </div>

          <Card className="p-6">
            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="space-y-2">
                <label htmlFor="topic" className="text-sm font-medium">
                  Video Topic
                </label>
                <Input
                  id="topic"
                  placeholder="Enter your video topic"
                  value={topic}
                  onChange={(e) => setTopic(e.target.value)}
                  required
                />
              </div>

              <div className="space-y-2">
                <label htmlFor="background" className="text-sm font-medium">
                  Background Description
                </label>
                <Textarea
                  id="background"
                  placeholder="Describe the desired background for your video"
                  value={background}
                  onChange={(e) => setBackground(e.target.value)}
                  required
                  className="min-h-[100px]"
                />
              </div>

              <Button
                type="submit"
                className="w-full"
                disabled={loading}
                size="lg"
              >
                {loading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Generating Video...
                  </>
                ) : (
                  <>
                    <VideoIcon className="mr-2 h-4 w-4" />
                    Generate Video
                  </>
                )}
              </Button>
            </form>
          </Card>

          {videoUrl && (
            <Card className="p-6 space-y-4">
              <h2 className="text-xl font-semibold">Generated Video</h2>
              <div className="aspect-video bg-muted rounded-lg overflow-hidden">
                <video
                  src={videoUrl}
                  controls
                  className="w-full h-full object-contain"
                />
              </div>
              <Button
                variant="outline"
                className="w-full"
                onClick={() => window.open(videoUrl, "_blank")}
              >
                <Download className="mr-2 h-4 w-4" />
                Download Video
              </Button>
            </Card>
          )}
        </div>
      </div>
    </main>
  );
}