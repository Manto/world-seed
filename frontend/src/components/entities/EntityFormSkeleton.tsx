import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';

export function EntityFormSkeleton() {
    return (
        <Card className="w-full max-w-2xl mx-auto" >
            <CardHeader>
                <Skeleton className="h-8 w-1/4" />
            </CardHeader>
            < CardContent className="space-y-6" >
                <div className="space-y-2" >
                    <Skeleton className="h-4 w-1/6" />
                    <Skeleton className="h-10 w-full" />
                </div>

                < div className="space-y-2" >
                    <Skeleton className="h-4 w-1/6" />
                    <Skeleton className="h-32 w-full" />
                </div>

                < div className="space-y-4" >
                    <Skeleton className="h-4 w-1/4" />
                    {
                        [...Array(3)].map((_, i) => (
                            <div key={i} className="space-y-2" >
                                <Skeleton className="h-4 w-1/6" />
                                <Skeleton className="h-10 w-full" />
                            </div>
                        ))
                    }
                </div>

                < div className="flex justify-end space-x-2" >
                    <Skeleton className="h-10 w-24" />
                    <Skeleton className="h-10 w-24" />
                </div>
            </CardContent>
        </Card>
    );
}