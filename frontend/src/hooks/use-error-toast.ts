import { useToast } from "./use-toast";
import { useCallback } from "react";

export function useErrorToast() {
  const { toast } = useToast();

  const showError = useCallback(
    (message: string) => {
      toast({
        variant: "destructive",
        title: "Error",
        description: message,
        duration: 5000,
      });
    },
    [toast]
  );

  return { showError };
}
